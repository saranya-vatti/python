var likesObj = {};
var done = {};
var sectionObj = {};
sectionObj["section1"] = {};
sectionObj["section2"] = {};
sectionObj["section3"] = {};
sectionObj["section4"] = {};

function tmp() {
    var arr = document.getElementsByClassName("v1Nh3 kIKUG  _bz0w");
    for(var i=0;i<arr.length;i++) {
        elem = document.getElementsByClassName("v1Nh3 kIKUG  _bz0w")[i].children[0];
        if(!done[elem.href]) {
            done[elem.href] = true;
            elem.click();
            window.setTimeout(function() {
                username = document.getElementsByClassName("nJAzx")[0].title;
                var likes = parseInt(document.getElementsByClassName("Nm9Fw")[0].children[0].children[0].textContent);
                var commentArr = document.getElementsByClassName("lnrre");
                var comments = 0;
                if(commentArr.length <= 0) {
                    comments = document.getElementsByClassName("_6lAjh").length-1;
                } else {
                    var button = document.getElementsByClassName("lnrre")[0].children[0];
                    if(!document.getElementsByClassName("lnrre")[0].children[0].children[0]) {
                        button.click();
                        debugger;
                    }
                    comments = parseInt(document.getElementsByClassName("lnrre")[0].children[0].children[0].textContent)*5
                }
                
                var total  = likes+comments;
                aArr = document.getElementsByTagName("a");
                for(var i=0;i<aArr.length;i++) {
                    if(aArr[i].href == "https://www.instagram.com/explore/tags/section1/") {
                        if(!sectionObj["section1"][username]) {
                            sectionObj["section1"][username] = {};
                            sectionObj["section1"][username]["likes"] = 0;
                            sectionObj["section1"][username]["comments"] = 0;
                            sectionObj["section1"][username]["total"] = 0;
                        }
                        sectionObj["section1"][username]["likes"] = sectionObj["section1"][username]["likes"] + likes;
                        sectionObj["section1"][username]["comments"] = sectionObj["section1"][username]["comments"] + comments;
                        sectionObj["section1"][username]["total"] = sectionObj["section1"][username]["total"] + total;
                        break;
                    } else if(aArr[i].href == "https://www.instagram.com/explore/tags/section2/") {
                        if(!sectionObj["section2"][username]) {
                            sectionObj["section2"][username] = {};
                            sectionObj["section2"][username]["likes"] = 0;
                            sectionObj["section2"][username]["comments"] = 0;
                            sectionObj["section2"][username]["total"] = 0;
                        }
                        sectionObj["section2"][username]["likes"] = sectionObj["section2"][username]["likes"] + likes;
                        sectionObj["section2"][username]["comments"] = sectionObj["section2"][username]["likes"] + comments;
                        sectionObj["section2"][username]["total"] = sectionObj["section2"][username]["total"] + total;
                        break;
                    } else if(aArr[i].href == "https://www.instagram.com/explore/tags/section3/") {
                        if(!sectionObj["section3"][username]) {
                            sectionObj["section3"][username] = {};
                            sectionObj["section3"][username]["likes"] = 0;
                            sectionObj["section3"][username]["comments"] = 0;
                            sectionObj["section3"][username]["total"] = 0;
                        }
                        sectionObj["section3"][username]["likes"] = sectionObj["section3"][username]["likes"] + likes;
                        sectionObj["section3"][username]["comments"] = sectionObj["section3"][username]["comments"] + comments;
                        sectionObj["section3"][username]["total"] = sectionObj["section3"][username]["total"] + total;
                        break;
                    } else if(aArr[i].href == "https://www.instagram.com/explore/tags/section4/") {
                        if(!sectionObj["section4"][username]) {
                            sectionObj["section4"][username] = {};
                            sectionObj["section4"][username]["likes"] = 0;
                            sectionObj["section4"][username]["comments"] = 0;
                            sectionObj["section4"][username]["total"] = 0;
                        }
                        sectionObj["section4"][username]["likes"] = sectionObj["section4"][username]["likes"] + likes;
                        sectionObj["section4"][username]["comments"] = sectionObj["section4"][username]["comments"] + comments;
                        sectionObj["section4"][username]["total"] = sectionObj["section4"][username]["total"] + total;
                        break;
                    }
                }
                
                document.getElementsByClassName("ckWGn")[0].click();
                window.setTimeout(function() {
                    tmp();
                    console.log(sectionObj);
                }, 1000);
            }, 3000);
            break;
        }
    }
}
tmp();

function tally() {
    var sectionTally = {};
    for(var section in sectionObj){
        var score = 0;
        for(var user in sectionObj[section]) {
            score += parseInt(sectionObj[section][user]["total"]);
        }
        sectionTally[section] = score;
    }
    console.log(sectionTally);
}