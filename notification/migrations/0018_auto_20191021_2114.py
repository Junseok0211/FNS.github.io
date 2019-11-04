# Generated by Django 2.1.8 on 2019-10-21 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0017_auto_20191021_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('joinTeam', 'joinTeam'), ('personalApply', 'personalApply'), ('teamComment', 'teamComment'), ('leagueComment', 'leagueComment'), ('leaguePersonalApply', 'leaguePersonalApply'), ('leagueTeamApply', 'leagueTeamApply'), ('personalReply', 'personalReply'), ('recruitingReply', 'recruitingReply'), ('teamReply', 'teamReply'), ('leagueReply', 'leagueReply'), ('recruitingApply', 'recruitingApply'), ('recruitingComment', 'recruitingComment'), ('recruitingAccepted', 'recruitingAccepted'), ('teamMatchingApply', 'teamMatchingApply'), ('suggestTeamMatching', 'suggestTeamMatching'), ('prComment', 'prComment'), ('teamAccepted', 'teamAccepted')], max_length=20),
        ),
    ]