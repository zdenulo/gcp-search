import os
import csv
import random

from locust import HttpLocust, TaskSet, task

words_all = []

with open(os.path.join(os.path.dirname(__file__), 'words.csv')) as f:
    csv_reader = csv.DictReader(f, fieldnames=('word', 'count'))
    for line in csv_reader:
        words_all.append(line['word'])
    words = words_all[0:5000] + words_all[-5000:]


class MyTaskSet(TaskSet):
    @task
    def my_task(self):
        w = random.choice(words)
        url = '/search?q={}'.format(w)
        self.client.get(url, name='search')


class MyLocust(HttpLocust):
    task_set = MyTaskSet
    min_wait = 1000
    max_wait = 5000
