import re
import os
from typing import Dict, Tuple, Optional, Any
from github import Github, Auth
from github.GithubException import GithubException
from github.Commit import Commit
from github.Repository import Repository
from .logging import get_logger

# Set up logger
logger = get_logger(__name__)

# Initialize GitHub client with authentication token if available
github_token = os.environ.get('GITHUB_TOKEN')
if github_token:
    # Use the newer authentication method to avoid deprecation warning
    auth = Auth.Token(github_token)
    github_client = Github(auth=auth)
    logger.info("Initialized GitHub client with authentication token")
else:
    github_client = Github()
    logger.warning("No GITHUB_TOKEN found. Using unauthenticated GitHub client", 
                  warning="subject to rate limits")

def parse_github_url(github_url: str) -> Tuple[str, str, str]:
    """
    Parse a GitHub URL to extract owner, repo, and commit SHA.
    
    Args:
        github_url: URL to a GitHub commit (e.g., https://github.com/owner/repo/commit/sha)
        
    Returns:
        Tuple of (owner, repo_name, commit_sha)
    """
    # Pattern for GitHub commit URLs
    pattern = r"https?://github\.com/([^/]+)/([^/]+)/commit/([^/]+)"
    match = re.match(pattern, github_url)
    
    if not match:
        logger.error("Failed to parse GitHub URL", url=github_url)
        raise ValueError(f"Invalid GitHub commit URL: {github_url}")
    
    owner, repo, commit_sha = match.groups()
    logger.debug("Successfully parsed GitHub URL", 
                owner=owner, repo=repo, commit_sha=commit_sha)
    return owner, repo, commit_sha

def get_repo(owner: str, repo: str) -> Repository:
    """
    Get a GitHub repository object.
    
    Args:
        owner: Repository owner
        repo: Repository name
        
    Returns:
        GitHub Repository object
    """
    logger.debug("Fetching GitHub repository", owner=owner, repo=repo)
    try:
        return github_client.get_repo(f"{owner}/{repo}")
    except GithubException as e:
        logger.error("Failed to get repository", 
                    owner=owner, repo=repo, 
                    error=str(e), status=e.status)
        raise ValueError(f"Failed to get repository {owner}/{repo}: {e}")

def get_commit(owner: str, repo: str, commit_sha: str) -> Commit:
    """
    Get a GitHub commit object.
    
    Args:
        owner: Repository owner
        repo: Repository name
        commit_sha: Commit SHA
        
    Returns:
        GitHub Commit object
    """
    logger.debug("Fetching GitHub commit", 
                owner=owner, repo=repo, commit_sha=commit_sha)
    try:
        repository = get_repo(owner, repo)
        return repository.get_commit(commit_sha)
    except GithubException as e:
        logger.error("Failed to get commit", 
                    owner=owner, repo=repo, commit_sha=commit_sha,
                    error=str(e), status=e.status)
        raise ValueError(f"Failed to get commit {commit_sha}: {e}")

def get_commit_data(owner: str, repo: str, commit_sha: str) -> Dict[str, Any]:
    """
    Get commit data from GitHub API.
    
    Args:
        owner: Repository owner
        repo: Repository name
        commit_sha: Commit SHA
        
    Returns:
        Dictionary containing commit data
    """
    commit = get_commit(owner, repo, commit_sha)
    logger.debug("Processing commit data", 
                commit_sha=commit_sha, 
                message=commit.commit.message[:50])
    
    # Convert commit object to dictionary with essential information
    files_data = []
    for file in commit.files:
        file_dict = {
            'filename': file.filename,
            'status': file.status,
            'additions': file.additions,
            'deletions': file.deletions,
            'changes': file.changes,
            'patch': file.patch if hasattr(file, 'patch') else None
        }
        files_data.append(file_dict)
    
    # Construct unified commit data
    commit_data = {
        'sha': commit.sha,
        'commit': {
            'message': commit.commit.message,
            'author': {
                'name': commit.commit.author.name,
                'date': commit.commit.author.date.isoformat()
            },
            'committer': {
                'name': commit.commit.committer.name,
                'date': commit.commit.committer.date.isoformat()
            }
        },
        'files': files_data,
        'stats': {
            'additions': commit.stats.additions,
            'deletions': commit.stats.deletions,
            'total': commit.stats.total
        },
        'parents': [{'sha': parent.sha} for parent in commit.parents]
    }
    
    logger.info("Retrieved commit data", 
               commit_sha=commit_sha, 
               files_count=len(files_data),
               additions=commit.stats.additions,
               deletions=commit.stats.deletions)
    return commit_data

def get_file_content(owner: str, repo: str, file_path: str, ref: str) -> Optional[str]:
    """
    Get content of a file at a specific commit from GitHub API.
    
    Args:
        owner: Repository owner
        repo: Repository name
        file_path: Path to file in the repository
        ref: Commit SHA or branch name
        
    Returns:
        Content of the file as string, or None if file doesn't exist
    """
    logger.debug("Fetching file content", 
                owner=owner, repo=repo, file_path=file_path, ref=ref)
    try:
        repository = get_repo(owner, repo)
        content_file = repository.get_contents(file_path, ref=ref)
        
        # Handle case where content_file might be a list (for directories)
        if isinstance(content_file, list):
            logger.debug("Content is a directory, not a file", file_path=file_path)
            return None
        
        content = content_file.decoded_content.decode('utf-8')
        logger.debug("Successfully fetched file content", 
                    file_path=file_path, 
                    content_size=len(content),
                    ref=ref)
        return content
    except GithubException as e:
        if e.status == 404:
            logger.debug("File not found", file_path=file_path, ref=ref)
            return None
        logger.error("Failed to get file content", 
                    file_path=file_path, ref=ref,
                    error=str(e), status=e.status)
        raise ValueError(f"Failed to get file content for {file_path} at {ref}: {e}")

def get_file_content_before_after(owner: str, repo: str, commit_sha: str, file_path: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Get the content of a file before and after a commit.
    
    Args:
        owner: Repository owner
        repo: Repository name
        file_path: Path to file in the repository
        commit_sha: SHA of the commit
        
    Returns:
        Tuple of (content_before, content_after)
    """
    logger.debug("Fetching file content before and after commit", 
                file_path=file_path, commit_sha=commit_sha)
    commit = get_commit(owner, repo, commit_sha)
    
    # Get parent commit SHA
    parent_sha = commit.parents[0].sha if commit.parents else None
    if parent_sha:
        logger.debug("Found parent commit", parent_sha=parent_sha)
    else:
        logger.debug("No parent commit found", commit_sha=commit_sha)
    
    # Get content after the commit
    after_content = get_file_content(owner, repo, file_path, commit_sha)
    
    # Get content before the commit (if parent exists)
    before_content = None
    if parent_sha:
        before_content = get_file_content(owner, repo, file_path, parent_sha)
    
    if before_content and after_content:
        logger.debug("Retrieved file content before and after commit", 
                    file_path=file_path, 
                    before_size=len(before_content),
                    after_size=len(after_content))
    elif after_content:
        logger.debug("Retrieved only after content (file added)", 
                    file_path=file_path, 
                    after_size=len(after_content))
    elif before_content:
        logger.debug("Retrieved only before content (file deleted)", 
                    file_path=file_path, 
                    before_size=len(before_content))
    else:
        logger.warning("Failed to retrieve file content", file_path=file_path)
    
    return before_content, after_content 