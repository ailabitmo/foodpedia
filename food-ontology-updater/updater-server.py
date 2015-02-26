import http.client
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import subprocess
import shutil


PORT = 80
REPOSITORY_NAME = 'ailabitmo/food-ontology'
LATEST_FOOD_OWL_URI = 'https://raw.githubusercontent.com/{0}/master/food.owl'.format(REPOSITORY_NAME)
GITHUB_URI = 'git@github.com:{0}.git'.format(REPOSITORY_NAME)
COMMIT_MESSAGE = 'updated index.html automatically '
GIT_WORKDIR = REPOSITORY_NAME.split('/')[-1]
ENCODING = 'utf-8'


class WebHookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.log_request()
        self.send_response(200)
        payload_json = json.loads(self.rfile.read().decode(ENCODING))
        commits_json_array = payload_json['commits']
        if check_if_food_owl_was_changed(commits_json_array):
            self.log_message('food.owl was changed')
            clone_repository(GITHUB_URI, GIT_WORKDIR)
            update_index_html(GIT_WORKDIR)
            commit_changes(GIT_WORKDIR, COMMIT_MESSAGE)
        else:
            self.log_message('food.owl wat NOT changed')
        self.log_message(str(commits_json_array))


def check_if_food_owl_was_changed(commits_json_array):
    return any(food_owl_in_commit(commit_json) for commit_json in commits_json_array)


def food_owl_in_commit(commit_json):
    return 'food.owl' in commit_json.get('modified', [])


def clone_repository(uri=GITHUB_URI, destination_dir=GIT_WORKDIR):
    shutil.rmtree(destination_dir, ignore_errors=True)
    subprocess.call(["git", "clone", "-b", "gh-pages", uri])


def update_index_html(workdir):
    index_html_path = r'./{0}/index.html'.format(workdir)
    index_html_str = generate_index_html_str()
    print(index_html_str)
    with open(index_html_path, 'w') as f:
        f.write(index_html_str)


def generate_index_html_str():
    conn = http.client.HTTPConnection("www.essepuntato.it")
    conn.request("GET", "/lode/{0}".format(LATEST_FOOD_OWL_URI))
    resp = conn.getresponse()
    index_html = resp.read().decode(ENCODING)
    conn.close()
    return index_html


def commit_changes(workdir=GIT_WORKDIR, message=COMMIT_MESSAGE):
    subprocess.call(["git", "-C", workdir, "commit", "-a", "-m", message])
    subprocess.call(["git", "-C", workdir, "push"])


def main():
    httpd = HTTPServer(("", PORT), WebHookHandler)

    print("start server which updates index.html on github pages on every commit to food.owl")
    print("serving at port {0}".format(PORT))
    httpd.serve_forever()


if __name__ == "__main__":
    main()
