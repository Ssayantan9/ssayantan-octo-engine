
from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear existing data using pymongo for robust deletion
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']
        db.leaderboard.delete_many({})
        db.activity.delete_many({})
        db.workout.delete_many({})
        db.user.delete_many({})
        db.team.delete_many({})

        # Create Teams
        marvel = Team.objects.create(name='marvel', description='Marvel Team')
        dc = Team.objects.create(name='dc', description='DC Team')

        # Create Users
        tony = User.objects.create(name='Tony Stark', email='tony@marvel.com', team=marvel.name)
        steve = User.objects.create(name='Steve Rogers', email='steve@marvel.com', team=marvel.name)
        bruce = User.objects.create(name='Bruce Wayne', email='bruce@dc.com', team=dc.name)
        clark = User.objects.create(name='Clark Kent', email='clark@dc.com', team=dc.name)

        # Create Workouts
        w1 = Workout.objects.create(name='Super Strength', description='Strength workout', suggested_for='marvel')
        w2 = Workout.objects.create(name='Flight Training', description='Flight workout', suggested_for='dc')

        # Create Activities
        Activity.objects.create(user=tony, type='run', duration=30, date=timezone.now().date())
        Activity.objects.create(user=steve, type='swim', duration=45, date=timezone.now().date())
        Activity.objects.create(user=bruce, type='cycle', duration=60, date=timezone.now().date())
        Activity.objects.create(user=clark, type='fly', duration=90, date=timezone.now().date())

        # Create Leaderboard
        Leaderboard.objects.create(user=tony, score=120, rank=1)
        Leaderboard.objects.create(user=steve, score=110, rank=2)
        Leaderboard.objects.create(user=bruce, score=100, rank=3)
        Leaderboard.objects.create(user=clark, score=90, rank=4)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data.'))
