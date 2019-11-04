# Generated by Django 2.1.8 on 2019-10-28 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0019_auto_20191021_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('joinTeam', 'joinTeam'), ('personalReply', 'personalReply'), ('leagueTeamApply', 'leagueTeamApply'), ('recruitingReply', 'recruitingReply'), ('leagueReply', 'leagueReply'), ('prComment', 'prComment'), ('recruitingComment', 'recruitingComment'), ('teamComment', 'teamComment'), ('leagueComment', 'leagueComment'), ('teamMatchingApply', 'teamMatchingApply'), ('teamReply', 'teamReply'), ('recruitingAccepted', 'recruitingAccepted'), ('leaguePersonalApply', 'leaguePersonalApply'), ('recruitingApply', 'recruitingApply'), ('suggestTeamMatching', 'suggestTeamMatching'), ('personalApply', 'personalApply'), ('teamAccepted', 'teamAccepted')], max_length=20),
        ),
    ]