from django.shortcuts import render, get_object_or_404
from decidedMatch.models import DecidedMatch
from django import template
from team.models import Team
from result.models import Result, AttendedPlayer, ScoredPlayer
from account.models import FNSUser
import datetime
# Create your views here.
register = template.Library()

def result(request):
    result = Result.objects.filter(confirm = True).order_by('-timeFrom')
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    notification = fnsuser.to.all().order_by('-created')
    countNotification = notification.filter(userCheck = False).count()    
    

    return render(request, 'result.html', {'result':result, 'countNotification':countNotification, 
    'notification':notification, 'fnsuser':fnsuser})

def input(request, decidedMatch_id):
    decidedMatch = get_object_or_404(DecidedMatch, pk = decidedMatch_id)
    myTeam = decidedMatch.myTeam.member.all()
    vsTeam = decidedMatch.vsTeam.member.all()
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    notification = fnsuser.to.all().order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
 

    if fnsuser != decidedMatch.myTeam.teamleader and fnsuser != decidedMatch.vsTeam.teamleader:
        message = '팀주장만 결과를 입력할 수 있습니다.'
        return render(request, 'decidedDetail.html', {'message':message, 'fnsuser':fnsuser, 
        'countNotification':countNotification, 'notification':notification, 'decidedMatch': decidedMatch})

    return render(request, 'input.html', {'fnsuser':fnsuser, 'decidedMatch': decidedMatch, 'myTeam':myTeam, 
    'countNotification':countNotification, 'notification':notification, 'vsTeam':vsTeam})


def inputScorer(request):
    attendedPlayer_id = request.POST.getlist('attendedPlayer_id[]')
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    notification = fnsuser.to.all().order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    decidedMatch_id = request.POST.get('decidedMatch_id')
    decidedMatch = get_object_or_404(DecidedMatch, pk = decidedMatch_id)
    myTeamScore = request.POST.get('myTeamScore')
    vsTeamScore = request.POST.get('vsTeamScore')

    if fnsuser != decidedMatch.myTeam.teamleader and fnsuser != decidedMatch.vsTeam.teamleader:
        message = '팀주장만 결과를 입력할 수 있습니다.'
        return render(request, 'decidedDetail.html', {'message':message, 'fnsuser':fnsuser, 
        'countNotification':countNotification, 'notification':notification, 'decidedMatch': decidedMatch})


    attendedPlayer = []
    num = 1
    for pk in attendedPlayer_id:
        user = get_object_or_404(FNSUser, pk=pk)
        attendedPlayer.insert(num, user)
        num += 1

    if decidedMatch.myTeam.teamleader == fnsuser:
        score = []
        for i in range(0, int(myTeamScore)): 
            name = i+1
            score.insert(i, name)

    elif decidedMatch.vsTeam.teamleader == fnsuser:
        score = []
        for i in range(0, int(vsTeamScore)): 
            name = i+1
            score.insert(i, name)


    number = len(attendedPlayer)
    vsTeamScore = request.POST.get('vsTeamScore')
    test = request.POST.get('test')
    return render(request, 'inputScorer.html', 
    {'attendedPlayer_id':attendedPlayer_id, 'number':number, 'attendedPlayer': attendedPlayer , 'score': score, 
    'countNotification':countNotification, 'notification':notification, 'myTeamScore': myTeamScore, 
    'fnsuser':fnsuser, 'vsTeamScore': vsTeamScore , 'decidedMatch': decidedMatch})

def myTeamResult(request):
    decidedMatch_id = request.POST.get('decidedMatch_id')
    decidedMatch = get_object_or_404(DecidedMatch, pk = decidedMatch_id)
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    notification = fnsuser.to.all().order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    if decidedMatch.my_suggest == False and decidedMatch.vs_suggest == False:
        result = Result.objects.create()
    else: 
        result = get_object_or_404(Result, pk = decidedMatch.result.id)

    result.myTeam = decidedMatch.myTeam
    result.vsTeam = decidedMatch.vsTeam
    result.myTeamScore = request.POST.get('myTeamScore')
    result.vsTeamScore = request.POST.get('vsTeamScore')
    
    result.match = decidedMatch
    result.timeFrom = decidedMatch.timeFrom
    attendedPlayer_id = request.POST.getlist('attendedPlayer_id[]')
    number = len(attendedPlayer_id)
    num = 0
    for i in range(0, number):
        number = attendedPlayer_id[i]
        user = get_object_or_404(FNSUser, pk= number)
        attendedPlayer = AttendedPlayer.objects.create(player = user, team = user.teamname, match = decidedMatch.match)
        num+=1


    scorer = []
    if decidedMatch.myTeam.teamleader == fnsuser:
        num = result.myTeamScore
    elif decidedMatch.vsTeam.teamleader == fnsuser:
        num = result.vsTeamScore
    for i in range(1, int(num)+1):
        name = 'scorer' + str(i)
        pk = request.POST.get(name)
        
        if pk == 'ownGoal':
            scoredPlayer = ScoredPlayer.objects.create(player = None, team = fnsuser.teamname, match = decidedMatch.match)
        else:
            user = get_object_or_404(FNSUser, pk=pk)
            scoredPlayer = ScoredPlayer.objects.create(player = user, team = user.teamname, match = decidedMatch.match)

    if fnsuser == decidedMatch.myTeam.teamleader:
        decidedMatch.my_suggest = True
        result.myCheck = True
        if int(result.vsTeamScore) != ScoredPlayer.objects.filter(team = result.vsTeam, match = decidedMatch.match).count():
            if decidedMatch.vs_suggest == True:
                result.vsCheck = False
                decidedMatch.vs_confirm = False
                decidedMatch.vs_suggest = False
        else:
            result.vsCheck = True

    elif fnsuser == decidedMatch.vsTeam.teamleader:
        decidedMatch.vs_suggest = True
        result.vsCheck = True
        if int(result.myTeamScore) != ScoredPlayer.objects.filter(team = result.myTeam, match = decidedMatch.match).count():
            if decidedMatch.my_suggest == True:
                decidedMatch.my_confirm = False
                decidedMatch.my_suggest = False
                result.myCheck = False
                # myCheck가 False 면 myTeam에서 입력을 확인하고 수정해야 함.
        else:
            result.myCheck = True

    decidedMatch.save()
    
    result.save()
    matches = DecidedMatch.objects.all().order_by('-created')
    return render(request, 'decidedMatch.html', {'matches':matches ,'result':result, 'fnsuser':fnsuser,
    'countNotification':countNotification, 'notification':notification, 'decidedMatch':decidedMatch})
   
        
def edit(request, decidedMatch_id):
    decidedMatch = get_object_or_404(DecidedMatch, pk = decidedMatch_id)
    myTeam = decidedMatch.myTeam.member.all()
    vsTeam = decidedMatch.vsTeam.member.all()
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    notification = fnsuser.to.all().order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    attendedPlayer = AttendedPlayer.objects.filter(match = decidedMatch.match, team = fnsuser.teamname).all()
    return render(request, 'edit.html', {'myTeam':myTeam,'vsTeam':vsTeam,'fnsuser':fnsuser,
    'countNotification':countNotification, 'notification':notification, 'decidedMatch':decidedMatch, 'attendedPlayer':attendedPlayer})

def editScorer(request):
    attendedPlayer_id = request.POST.getlist('attendedPlayer_id[]')
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    notification = fnsuser.to.all().order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    decidedMatch_id = request.POST.get('decidedMatch_id')
    decidedMatch = get_object_or_404(DecidedMatch, pk = decidedMatch_id)
    myTeamScore = request.POST.get('myTeamScore')
    vsTeamScore = request.POST.get('vsTeamScore')
    if fnsuser != decidedMatch.myTeam.teamleader and fnsuser != decidedMatch.vsTeam.teamleader:
        message = '팀주장만 결과를 입력할 수 있습니다.'
        return render(request, 'decidedDetail.html', {'countNotification':countNotification, 'notification':notification, 
        'message':message, 'fnsuser':fnsuser, 'decidedMatch': decidedMatch})


    attendedPlayer = []
    num = 1
    for pk in attendedPlayer_id:
        user = get_object_or_404(FNSUser, pk=pk)
        attendedPlayer.insert(num, user)
        num += 1

    if decidedMatch.myTeam.teamleader == fnsuser:
        score = []
        for i in range(0, int(myTeamScore)): 
            name = i+1
            score.insert(i, name)

    elif decidedMatch.vsTeam.teamleader == fnsuser:
        score = []
        for i in range(0, int(vsTeamScore)): 
            name = i+1
            score.insert(i, name)


    number = len(attendedPlayer)
    vsTeamScore = request.POST.get('vsTeamScore')
    scoredPlayer = ScoredPlayer.objects.filter(match=decidedMatch.match, team = fnsuser.teamname).all()
    return render(request, 'editScorer.html', 
    {'countNotification':countNotification, 'notification':notification, 'scoredPlayer': scoredPlayer, 
    'attendedPlayer_id':attendedPlayer_id, 'number':number, 'attendedPlayer': attendedPlayer , 'score': score , 
    'fnsuser':fnsuser, 'myTeamScore': myTeamScore, 'vsTeamScore': vsTeamScore , 'decidedMatch': decidedMatch})


def editTeamResult(request):
    decidedMatch_id = request.POST.get('decidedMatch_id')
    decidedMatch = get_object_or_404(DecidedMatch, pk = decidedMatch_id)
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    notification = fnsuser.to.all().order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    result = get_object_or_404(Result, pk = decidedMatch.result.id)

    result.myTeamScore = request.POST.get('myTeamScore')
    result.vsTeamScore = request.POST.get('vsTeamScore')
    
    result.match = decidedMatch
    result.timeFrom = decidedMatch.timeFrom
    attendedPlayer_id = request.POST.getlist('attendedPlayer_id[]')
    number = len(attendedPlayer_id)
    num = 0
    preAttendedPlayer = AttendedPlayer.objects.filter(team = fnsuser.teamname, match = decidedMatch.match).order_by('created')
    preAttendedPlayer.delete()
    for i in range(0, number):
        number = attendedPlayer_id[i]
        user = get_object_or_404(FNSUser, pk= number)
        attendedPlayer = AttendedPlayer.objects.create(player = user, team = user.teamname, match = decidedMatch.match)
        num+=1


    scorer = []
    preScoredPlayer = ScoredPlayer.objects.filter(team = fnsuser.teamname, match = decidedMatch.match)
    preScoredPlayer.delete()
    if decidedMatch.myTeam.teamleader == fnsuser:
        num = result.myTeamScore
    elif decidedMatch.vsTeam.teamleader == fnsuser:
        num = result.vsTeamScore

    for i in range(1, int(num)+1):
        name = 'scorer' + str(i)
        pk = request.POST.get(name)
        
        if pk == 'ownGoal':
            scoredPlayer = ScoredPlayer.objects.create(player = None, team = fnsuser.teamname, match = decidedMatch.match)
        else:
            user = get_object_or_404(FNSUser, pk=pk)
            scoredPlayer = ScoredPlayer.objects.create(player = user, team = user.teamname, match = decidedMatch.match)

 
    if fnsuser == decidedMatch.myTeam.teamleader:
        decidedMatch.my_suggest = True
        decidedMatch.vs_confirm = False
        result.myCheck = True
        if int(result.vsTeamScore) != ScoredPlayer.objects.filter(team = result.vsTeam, match = decidedMatch.match).count():
            if decidedMatch.vs_suggest == True:
                result.vsCheck = False
                decidedMatch.vs_confirm = False
                decidedMatch.vs_suggest = False
        else:
            result.vsCheck = True
            

    elif fnsuser == decidedMatch.vsTeam.teamleader:
        decidedMatch.vs_suggest = True
        decidedMatch.my_confirm = False
        result.vsCheck = True
        if int(result.myTeamScore) != ScoredPlayer.objects.filter(team = result.myTeam, match = decidedMatch.match).count():
            if decidedMatch.my_suggest == True:
                decidedMatch.my_confirm = False
                decidedMatch.my_suggest = False
                result.myCheck = False
                # myCheck가 False 면 myTeam에서 입력을 확인하고 수정해야 함.
        else:
            result.myCheck = True
                
            

    decidedMatch.save()
    result.save()
    matches = DecidedMatch.objects.all().order_by('-created')
    return render(request, 'decidedMatch.html', {'countNotification':countNotification, 'notification':notification, 
    'fnsuser':fnsuser, 'matches':matches ,'result':result, 'decidedMatch':decidedMatch})


def myConfirm(request, decidedMatch_id):
    decidedMatch = get_object_or_404(DecidedMatch, pk = decidedMatch_id)
    decidedMatch.my_confirm = True
    decidedMatch.save()
    
    now = datetime.datetime.now()
    timeFrom = decidedMatch.timeFrom
    timeTo = decidedMatch.timeTo
    state = None
    if now < timeFrom:
        state = 'before'
    elif now > timeFrom and now < timeTo:
        state = "ing"
    elif now > timeTo:
        state = 'finished'

    myAttendedPlayer = AttendedPlayer.objects.filter(match = decidedMatch.match, team = decidedMatch.myTeam).all()
    vsAttendedPlayer = AttendedPlayer.objects.filter(match = decidedMatch.match, team = decidedMatch.vsTeam).all()
    myScoredPlayer = ScoredPlayer.objects.filter(match = decidedMatch.match, team = decidedMatch.myTeam).all()
    vsScoredPlayer = ScoredPlayer.objects.filter(match = decidedMatch.match, team = decidedMatch.vsTeam).all()
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    notification = fnsuser.to.all().order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    result = decidedMatch.result

    if decidedMatch.vs_confirm:
        decidedMatch.result.confirm = True
        decidedMatch.result.save()
        myTeamId = decidedMatch.myTeam.id
        myTeam = get_object_or_404(Team, pk = myTeamId)
        myTeam.gf = result.myTeamScore
        myTeam.ga = result.vsTeamScore
        myTeam.gd = int(result.myTeamScore - result.vsTeamScore)
        myTeam.matchcount += 1
        if (myTeam.gf > myTeam.ga):
            myTeam.win += 1
            myTeam.point += 3
        elif (myTeam.gf == myTeam.ga):
            myTeam.draw += 1
            myTeam.point += 1
        elif (myTeam.gf < myTeam.ga):
            myTeam.lose += 1

        myTeam.save()
        attendedPlayer = AttendedPlayer.objects.filter(team = decidedMatch.myTeam, match = decidedMatch.match).all()
        scoredPlayer = ScoredPlayer.objects.filter(team = decidedMatch.myTeam, match = decidedMatch.match).all()
        for player in attendedPlayer:
            user = player.player
            if user is not None:
                user.matchcount += 1
                user.save()

        for player in scoredPlayer:
            user = player.player
            if user is not None:
                user.score += 1
                user.save()
                
            goalAverage = float(user.score) / float(user.matchcount)
            average = round(goalAverage, 3)
            user.goalAverage = average
            user.save()

        vsTeamId = decidedMatch.vsTeam.id
        vsTeam = get_object_or_404(Team, pk = vsTeamId)
        vsTeam.gf = result.vsTeamScore
        vsTeam.ga = result.myTeamScore
        vsTeam.gd = int(result.vsTeamScore - result.myTeamScore)
        vsTeam.matchcount += 1
        if (vsTeam.gf > vsTeam.ga):
            vsTeam.win += 1
            vsTeam.point += 3
        elif (vsTeam.gf == vsTeam.ga):
            vsTeam.draw += 1
            vsTeam.point += 1
        elif (vsTeam.gf < vsTeam.ga):
            vsTeam.lose += 1

        vsTeam.save()
        attendedPlayer = AttendedPlayer.objects.filter(team = decidedMatch.vsTeam, match = decidedMatch.match).all()
        scoredPlayer = ScoredPlayer.objects.filter(team = decidedMatch.vsTeam, match = decidedMatch.match).all()
        for player in attendedPlayer:
            user = player.player
            if user is not None:
                user.matchcount += 1
                user.save()

        for player in scoredPlayer:
            user = player.player
            if user is not None:
                user.score += 1
                user.save()
                
            goalAverage = float(user.score) / float(user.matchcount)
            average = round(goalAverage, 3)
            user.goalAverage = average
            user.save()

    return render(request, 'decidedDetail.html', {'fnsuser':fnsuser, 'decidedMatch':decidedMatch, 'myAttendedPlayer':myAttendedPlayer,
    'state':state, 'countNotification':countNotification, 'notification':notification, 'vsAttendedPlayer':vsAttendedPlayer,'myScoredPlayer':myScoredPlayer,'vsScoredPlayer':vsScoredPlayer})

def vsConfirm(request, decidedMatch_id):
    decidedMatch = get_object_or_404(DecidedMatch, pk = decidedMatch_id)
    decidedMatch.vs_confirm = True
    decidedMatch.save()
    
    now = datetime.datetime.now()
    timeFrom = decidedMatch.timeFrom
    timeTo = decidedMatch.timeTo
    state = None
    if now < timeFrom:
        state = 'before'
    elif now > timeFrom and now < timeTo:
        state = "ing"
    elif now > timeTo:
        state = 'finished'

    myAttendedPlayer = AttendedPlayer.objects.filter(match = decidedMatch.match, team = decidedMatch.myTeam).all()
    vsAttendedPlayer = AttendedPlayer.objects.filter(match = decidedMatch.match, team = decidedMatch.vsTeam).all()
    myScoredPlayer = ScoredPlayer.objects.filter(match = decidedMatch.match, team = decidedMatch.myTeam).all()
    vsScoredPlayer = ScoredPlayer.objects.filter(match = decidedMatch.match, team = decidedMatch.vsTeam).all()
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    notification = fnsuser.to.all().order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    result = decidedMatch.result

    if decidedMatch.my_confirm:
        decidedMatch.result.confirm = True
        decidedMatch.result.save()
        myTeamId = decidedMatch.myTeam.id
        myTeam = get_object_or_404(Team, pk = myTeamId)
        myTeam.gf = result.myTeamScore
        myTeam.ga = result.vsTeamScore
        myTeam.gd = int(result.myTeamScore - result.vsTeamScore)
        myTeam.matchcount += 1
        if (myTeam.gf > myTeam.ga):
            myTeam.win += 1
            myTeam.point += 3
        elif (myTeam.gf == myTeam.ga):
            myTeam.draw += 1
            myTeam.point += 1
        elif (myTeam.gf < myTeam.ga):
            myTeam.lose += 1

        myTeam.save()
        attendedPlayer = AttendedPlayer.objects.filter(team = decidedMatch.myTeam, match = decidedMatch.match).all()
        scoredPlayer = ScoredPlayer.objects.filter(team = decidedMatch.myTeam, match = decidedMatch.match).all()
        for player in attendedPlayer:
            user = player.player
            if user is not None:
                user.matchcount += 1
                user.save()

        for player in scoredPlayer:
            user = player.player
            if user is not None:
                user.score += 1
                goalAverage = float(user.score) / float(user.matchcount)
                average = round(goalAverage, 3)
                user.goalAverage = average
                user.save()
                

        vsTeamId = decidedMatch.vsTeam.id
        vsTeam = get_object_or_404(Team, pk = vsTeamId)
        vsTeam.gf = result.vsTeamScore
        vsTeam.ga = result.myTeamScore
        vsTeam.gd = int(result.vsTeamScore - result.myTeamScore)
        vsTeam.matchcount += 1
        if (vsTeam.gf > vsTeam.ga):
            vsTeam.win += 1
            vsTeam.point += 3
        elif (vsTeam.gf == vsTeam.ga):
            vsTeam.draw += 1
            vsTeam.point += 1
        elif (vsTeam.gf < vsTeam.ga):
            vsTeam.lose += 1

        vsTeam.save()
        attendedPlayer = AttendedPlayer.objects.filter(team = decidedMatch.vsTeam, match = decidedMatch.match).all()
        scoredPlayer = ScoredPlayer.objects.filter(team = decidedMatch.vsTeam, match = decidedMatch.match).all()
        for player in attendedPlayer:
            user = player.player
            if user is not None:
                user.matchcount += 1
                user.save()

        for player in scoredPlayer:
            user = player.player
            if user is not None:
                user.score += 1
                goalAverage = float(user.score) / float(user.matchcount)
                average = round(goalAverage, 3)
                user.goalAverage = average
                user.save()
                
            

    return render(request, 'decidedDetail.html', {'fnsuser':fnsuser, 'decidedMatch':decidedMatch, 'myAttendedPlayer':myAttendedPlayer,
    'state':state, 'countNotification':countNotification, 'notification':notification, 'vsAttendedPlayer':vsAttendedPlayer,'myScoredPlayer':myScoredPlayer,'vsScoredPlayer':vsScoredPlayer})
    