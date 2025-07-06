import pytz
from django.core.management.base import BaseCommand

from temba.orgs.models import Org, OrgRole, User
from temba.settings import *


class Command(BaseCommand):  # pragma: no cover
    help = "Utility to manage admin user"

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, required=True)
        parser.add_argument('--email', type=str, required=True)
        parser.add_argument('--password', type=str, required=True)
        parser.add_argument('--root', action='store_true')

    def handle(self, *args, **options):
        name = options['username']
        email = options['email']
        password = options['password']
        is_superuser = options['root']
        user =  self.create_user(username=name, email=email, password=password, is_root=is_superuser)
        org = self.create_org(user)
        self.add_user_to_org(user, org)

    def create_user(self, username:str, email:str, password:str, is_root:bool=False)->User:
        user = User.objects.filter(username=username).first()
        if user:
            self.stdout.write(self.style.NOTICE(f"User {username} already exists, skipping ...")+"\n")
            return user
        self.stdout.write(f"Creating user {username} ... ")
        if is_root:
            user = User.objects.create_superuser(username, email, password)
        else:
            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)
        user.save()
        self.stdout.write(self.style.SUCCESS("OK") + "\n")
        return user

    def create_org(self, user:User)->Org:
        brand = self.default_brand
        if not brand:
            raise CommandError(f"Brand not found for the default organization {DEFAULT_BRAND}")
        name = brand['name']
        slug = brand['slug']
        topup =  brand['welcome_topup']
        org = Org.objects.filter(name=name).first()
        if not org:
            self.stdout.write(f"Creating organization {name} ... ")
            timezone = pytz.timezone(USER_TIME_ZONE)
            org = Org.objects.create(
                name=name,
                timezone=timezone,
                brand=slug,
                slug=slug,
                is_multi_user=True,
                is_multi_org=True,
                created_by=user,
                modified_by=user,
            )
            org.initialize(branding=brand, topup_size=topup)
        self.stdout.write(self.style.SUCCESS("OK") + "\n")
        return org

    def add_user_to_org(self, user:User, org:Org)->Org:
        self.stdout.write(f"Adding user {user.username} to org {org.name}")
        if org.has_user(user):
            self.stdout.write(self.style.NOTICE(f"User {user.username} already belongs to organization {org.name} ... ") + "\n")
            return org
        org.add_user(user, OrgRole.ADMINISTRATOR)
        org.add_user(user, OrgRole.EDITOR)
        org.save()
        self.stdout.write(self.style.SUCCESS("OK") + "\n")
        return  org

    @property
    def default_brand(self)->str:
        return BRANDING[DEFAULT_BRAND]
