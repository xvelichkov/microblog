from django.core.management.base import BaseCommand
from faker import Faker
import random
from tqdm import tqdm 
from apps.accounts.models import AccountUser
from apps.followers.models import Follower
from apps.posts.models import Post, Comment, Like
import csv

fake = Faker()

class Command(BaseCommand):
    help = 'Generates and imports example data to the database'

    def handle(self, *args, **kwargs):
        self.stdout.write('Generating example data...')

        users_credentials = []
        users = []
        for _ in tqdm(range(2), desc='Generating Users'):
           
            profile = fake.simple_profile()
            first_name = " ".join(profile["name"].split()[:-1])
            last_name = profile["name"].split()[-1]

            password = fake.password()
            user = AccountUser.objects.create_user(
                username=profile["username"],
                email=profile["mail"],
                password=password,
                first_name = first_name,
                last_name = last_name
            )

            users.append(user)
            users_credentials.append((profile["username"], password))
            

        with open('user_credentials.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Username', 'Password'])
            writer.writerows(users_credentials)


        for user in tqdm(users, desc='Generating Followers and Following'):
            num_followers = random.randint(0, (len(users)//2))
            followers = random.sample(list(AccountUser.objects.exclude(pk=user.pk)), num_followers)
            for follower in followers:
                print(user)
                print(follower)
                Follower.objects.create(user=user, follower=follower)

        for user in users:
            for _ in tqdm(range(50), desc=f'Generating Posts for User {user.username}'):
                post = Post.objects.create(
                    author=user,
                    body=fake.text(max_nb_chars=320),
                    image=fake.image_url(),
                )

                num_likes = random.randint(0, len(users) // 2)
                liked_users = random.sample(users, num_likes)
                for liked_user in liked_users:
                    Like.objects.create(post=post, user=liked_user)

                for _ in range(50):
                    Comment.objects.create(
                        author=random.choice(users),
                        body=fake.text(max_nb_chars=255),
                        post=post,
                    )

        self.stdout.write(self.style.SUCCESS('Example data generated and imported successfully.'))
