from git import Repo
import argparse
import colorama
from prettytable import PrettyTable
from rich.progress import Progress

colorama.init()

parser = argparse.ArgumentParser(description='Get command line arguments')
parser.add_argument('--contributors', action='store_true', help='Get contributors')
parser.add_argument('--commit-lines', action='store_true', help='Get commit lines')
parser.add_argument('-path', type=str, help='Path to the repository')
parser.add_argument('-since', type=str, help='Begin date')
parser.add_argument('-until', type=str, help='End date')

args = parser.parse_args()

path = args.path if args.path else '.'
git_params = ['--since=' + args.since, '--until=' + args.until] if args.since and args.until else []

print(colorama.Fore.GREEN + 'Path to the repository: ' + path + colorama.Style.RESET_ALL)

try:
    repo = Repo(path)
except:
    print(colorama.Fore.RED + 'Path does not exist' + colorama.Style.RESET_ALL)
    exit(1)


# 统计贡献者
if args.contributors:
    contributors = repo.git.shortlog('-sne', '--all', *git_params).split('\n')
    print(colorama.Fore.GREEN + 'Contributors:' + colorama.Style.RESET_ALL)
    with Progress(transient=True) as progress:
        task = progress.add_task('Processing', total=len(contributors))
        for contributor in contributors:
            progress.update(task, advance=1)
            print(colorama.Fore.BLUE + contributor + colorama.Style.RESET_ALL)


# 按贡献者统计提交行数，区分添加、删除
if args.commit_lines:
    contributors = repo.git.shortlog('-sne', '--all', *git_params).split('\n')
    if contributors == ['']:
        print(colorama.Fore.RED + 'No contributors found.' + colorama.Style.RESET_ALL)
        exit(0)

    print(colorama.Fore.GREEN + 'Commit lines:' + colorama.Style.RESET_ALL)
    table = PrettyTable()
    table.field_names = [f'{colorama.Fore.BLUE}Contributor{colorama.Style.RESET_ALL}', f'{colorama.Fore.GREEN}Additions{colorama.Style.RESET_ALL}', f'{colorama.Fore.RED}Deletions{colorama.Style.RESET_ALL}']

    with Progress(transient=True) as progress:
        task = progress.add_task('Processing', total=len(contributors))
        for contributor in contributors:
            contributor = contributor.split('\t')
            contributor_name = contributor[1].split(' ')[0]
            contributor_email = contributor[1].split(' ')[1][1:-1]
            contributor_commits = repo.git.log('--author=' + contributor_email, '--pretty=tformat:', '--numstat', *git_params).split('\n')
            contributor_additions = 0
            contributor_deletions = 0

            for commit in contributor_commits:
                commit = commit.split('\t')
                if len(commit) == 3 and commit[0].isdigit() and commit[1].isdigit():
                    contributor_additions += int(commit[0])
                    contributor_deletions += int(commit[1])
            table.add_row([f'{colorama.Fore.BLUE}{contributor_name}{colorama.Style.RESET_ALL}', f'{colorama.Fore.GREEN}{contributor_additions}{colorama.Style.RESET_ALL}', f'{colorama.Fore.RED}{contributor_deletions}{colorama.Style.RESET_ALL}'])
            progress.update(task, advance=1)
    
    print(table)