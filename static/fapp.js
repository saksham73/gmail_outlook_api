$(document).ready(function(){
    $(".button1").click(function(){
        var subject = $("#subject").val();
        var message = $("#message").val();
        var to = $("#to").val();
        var from = $("#from").val();
        console.log(subject);
        console.log(message);
        console.log(to);
        console.log(from);  

        gmail(subject,message,to,from)
    })

    $(".button2").click(function(){
        getgmail()
    })
    
    $(".button3").click(function(){

        var message = $("#messagem").val();

        postalwaysenabled(message)
    })

    $(".button4").click(function(){
        var message = $("#messagem").val();
        var from=$("#tom").val();
        var to=$("#fromm").val();
        postscheduled(message,from,to)
    })

    $(".button5").click(function(){


        postendvacation()
    })

    $(".button6").click(function(){


        getstats()
    })

    $(".gmailCal").click(function(){
        var to=$("#to").val();
        var from=$("#from").val();
        var desc=$("#desc").val();
        var summary=$("#sum").val();
        createGmailEvent(desc,summary,to,from)
    })

    $(".outlookCal").click(function(){
        var to=$("#tom").val();
        var from=$("#fromm").val();
        var desc=$("#descm").val();
        var summary=$("#summ").val();
        createoutlookEvent(desc,summary,to,from)
    })

    $(".bauth").click(function(){
        var link=$("#auth").val();
        execute(link)
    })
});

function gmail(subject,message,to,from){
    var d1=new Date(to);
    var d2=new Date(from);
    var utto=Math.floor(d1.getTime());
    var utfrom=Math.floor(d2.getTime());
    /*if(utto=NaN){
        utto=0000000000000;
    }
    if(utfrom=NaN){
        utfrom=0000000000000;
    }*/
    console.log(utto);
    console.log(utfrom);
    data={
        'enableAutoReply' : 'True',
        'responseSubject': subject,
        'responseBodyHtml': message,
        "startTime": utto,
        "endTime": utfrom
    }
    var xhttp=new XMLHttpRequest();
    xhttp.open("POST","/googleauth",true);
    xhttp.setRequestHeader('Content-Type','application/json');
    xhttp.send(JSON.stringify(data));
    
}


function getgmail(){
    var xhttp=new XMLHttpRequest();
    xhttp.onreadystatechange=function(){
        if(this.status==200 && this.readyState==4)
        {
            //console.log("success")
            var info=JSON.parse(this.responseText)
            console.log(info)
            document.getElementById("para").innerHTML =JSON.stringify(info);
        }
    };
    xhttp.open("GET","/googleauth",true);
    xhttp.setRequestHeader('Content-Type','application/json');
    xhttp.send();
    
}

function postalwaysenabled(message){
    var mes=message;
    console.log(mes)
    data={
        'status': 'alwaysEnabled',
        "internalReplyMessage": mes,
        "externalReplyMessage": mes
    }
    var xhttp=new XMLHttpRequest();
    xhttp.open("POST","/microauth",true);
    xhttp.setRequestHeader('Content-Type','application/json');
    xhttp.send(JSON.stringify(data));
}

function postendvacation(){
    data={
        'status': 'disabled',
        "internalReplyMessage": '',
        "externalReplyMessage": ''
    }
    var xhttp=new XMLHttpRequest();
    xhttp.open("POST","/microauth",true);
    xhttp.setRequestHeader('Content-Type','application/json');
    xhttp.send(JSON.stringify(data));
}

function getstats(){
    var xhttp=new XMLHttpRequest();
    xhttp.onreadystatechange=function(){
        if(this.status==200 && this.readyState==4)
        {
            //console.log("success")
            var info=JSON.parse(this.responseText)
            console.log(info)
            document.getElementById("para2").innerHTML =JSON.stringify(info);
        }
    };
    xhttp.open("GET","/microauth",true);
    xhttp.setRequestHeader('Content-Type','application/json');
    xhttp.send();
    
}

function postscheduled(message,from,to){
    var mes=message;
    var fromdate=from+'T00:30:00.0000000';
    var todate=to+'T23:59:59.0000000';
    data={
        "status": "Scheduled",
        "internalReplyMessage": mes,
        "externalReplyMessage": mes,
        "scheduledStartDateTime": {
            "dateTime": fromdate,
            "timeZone": "Asia/Kolkata"
        },
        "scheduledEndDateTime": {
            "dateTime": todate,
            "timeZone": "Asia/Kolkata"
        }
    }
    var xhttp=new XMLHttpRequest();
    xhttp.open("POST","/microauth",true);
    xhttp.setRequestHeader('Content-Type','application/json');
    xhttp.send(JSON.stringify(data));
}

function createGmailEvent(desc,summary,to,from){
    var todate=to;
    newto=todate.replace(/\./g, '-');
    var fromdate=from;
    newfrom=fromdate.replace(/\./g, '-');
    var des=desc;
    var summary=summary;
    console.log(newto)
    console.log(newfrom)
    console.log(des);
    console.log(summary)
    data = {
        "end": {
            "date": newfrom,
            "timeZone": "Asia/Kolkata"
        },
        "start": {
            "date": newto,
            "timeZone": "Asia/Kolkata"
        },
        "description": des,
        "summary": summary
        }
    var xhttp=new XMLHttpRequest();
    xhttp.open("POST","/gmailcal",true);
    xhttp.setRequestHeader('Content-Type','application/json');
    xhttp.send(JSON.stringify(data));
}

function createoutlookEvent(desc,summary,to,from){
    var todate=to+'T00:30:00.0000000';
    var fromdate=from+'T23:59:59.0000000';
    var des=desc;
    var summary=summary;
    console.log(todate)
    console.log(fromdate)
    console.log(des);
    console.log(summary)
    data = {
            "subject": des,
            "body": {
                "contentType": "HTML",
                "content": summary
            },
            "start": {
                "dateTime": todate,
                "timeZone": "Asia/Kolkata"
            },
            "end": {
                "dateTime": fromdate,
                "timeZone": "Asia/Kolkata"
            }
        }
    var xhttp=new XMLHttpRequest();
    xhttp.open("POST","/outlookcal",true);
    xhttp.setRequestHeader('Content-Type','application/json');
    xhttp.send(JSON.stringify(data));
}

function execute(command) {
    var link =command
    console.log(link)
    data={
        'val': link
    }
    var xhttp=new XMLHttpRequest();
    xhttp.open("POST","/putinterminal",true);
    xhttp.setRequestHeader('Content-Type','application/json');
    xhttp.send(JSON.stringify(data));
  }