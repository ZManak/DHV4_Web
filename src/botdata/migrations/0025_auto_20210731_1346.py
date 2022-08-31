# Generated by Django 3.2.5 on 2021-07-31 13:46

from django.db import migrations


def setup_member_from_user_on_support_server(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    LandminesUserData = apps.get_model('botdata', 'LandminesUserData')
    DiscordMember = apps.get_model('botdata', 'DiscordMember')
    DiscordGuild = apps.get_model('botdata', 'DiscordGuild')
    try:
        dh_guild = DiscordGuild.objects.get(discord_id=195260081036591104)
    except:
        return

    for userdata in LandminesUserData.objects.all():
        user = userdata.user
        member, _ = DiscordMember.objects.all().get_or_create(user=user, guild=dh_guild)
        userdata.member = member
        userdata.save()


def remove_members(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    LandminesUserData = apps.get_model('botdata', 'LandminesUserData')
    LandminesUserData.objects.all().update(member=None)


class Migration(migrations.Migration):

    dependencies = [
        ('botdata', '0024_landminesuserdata_member'),
    ]

    operations = [
        migrations.RunPython(setup_member_from_user_on_support_server, remove_members),
    ]
