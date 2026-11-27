import json
AT=10960237; GD=10964284; HOOK=3115801
BASE="app0Nha03xdrY2lVM"; TBL="tblLPl2mWeAi48UKn"; RES="fldKE3JlEbRHryhvU"
D='{{formatDate(now; "MM.DD.YY")}}'
pos=[0]
def dz():
    pos[0]+=300; return {"designer":{"x":pos[0],"y":0}}
def upd(i,text):
    return {"id":i,"module":"airtable:ActionUpdateRecords","version":3,"parameters":{"__IMTCONN__":AT},
      "mapper":{"id":"{{1.id}}","base":BASE,"table":TBL,"record":{RES:text},"typecast":False,"useColumnId":True},"metadata":dz()}
def ign(i): return {"id":i,"module":"builtin:Ignore","version":1,"metadata":dz()}
def drive(i,url,qs,errtext=None):
    m={"id":i,"module":"google-drive:makeApiCall","version":4,"parameters":{"__IMTCONN__":GD},
       "mapper":{"url":url,"method":"GET","headers":[{"key":"Content-Type","value":"application/json"}],
                 "qs":[{"key":k,"value":v} for k,v in qs]},"metadata":dz()}
    if errtext: m["onerror"]=[upd(i*10+1,errtext.replace("#",str(i))),ign(i*10+2)]
    return m
def flt(name,conds): return {"name":name,"conditions":conds}
LINK="{{1.`Google Link`}}"
PAT="^https://(docs|drive)\\.google\\.com/.*(/d/|[?&]id=)[A-Za-z0-9_-]{20,}"
FID='{{ifempty(first(split(first(split(get(split(1.`Google Link`; "/d/"); 2); "/")); "?")); first(split(get(split(1.`Google Link`; "id="); 2); "&")))}}'
FF="id,name,mimeType,parents,driveId,trashed"
walkerr="Not done "+D+": Drive refused while looking for this file's Archive folder ({{#.error.message}}). Nothing was changed."
P=["{{first(3.body.parents)}}"]+["{{ifempty(first(%d.body.parents); %d.body.id)}}"%(n,n) for n in (11,12,13,14)]
def lst(i,p):
    return drive(i,"/v3/files",[("q","'%s' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false and (name contains '09_Archive' or name = 'Archive')"%p),
      ("supportsAllDrives","true"),("includeItemsFromAllDrives","true"),("corpora","allDrives"),("fields","files(id,name)")],walkerr)
def pick(key):
    e='first(map(25.body.files; "%s"))'%key
    for n in (24,23,22,21): e='ifempty(first(map(%d.body.files; "%s")); %s)'%(n,key,e)
    return "{{"+e+"}}"
def comp(i,v): return {"id":i,"module":"util:ComposeTransformer","version":1,"mapper":{"value":v},"metadata":dz()}
def call(i,scn,data): return {"id":i,"module":"scenario-service:CallSubscenario","version":2,
    "parameters":{"scenario":scn,"shouldWaitForExecutionEnd":True},"mapper":{"data":data},"metadata":dz()}
def ifd(n,a,b): return '{{if(%d.result = "Done"; %s; %s)}}'%(n,a,b)
NEWNAME='{{if(substring(3.body.name; 0; 8) = "Retired_"; 3.body.name; 29.value)}}'

trash_txt=ifd(5,'"Put in Drive\'s trash "','"Not done "')+D+ifd(5,'". Drive read it back as trashed: "','": "')+ifd(5,"5.trashed","5.error")+ifd(5,'". Drive keeps it 30 days, so it can be restored until then."','""')
arch_txt=ifd(7,'"Archived "','"Not done "')+D+ifd(7,'": moved into the folder \'"','": "')+ifd(7,"27.value","7.error")+ifd(7,'"\' and renamed \'"','""')+ifd(7,"7.name",'""')+ifd(7,'"\'. The link still opens it."','""')
inarch_txt=ifd(9,'"Archived "','"Not done "')+D+ifd(9,'": already inside the archive folder \'"','": "')+ifd(9,"33.value","9.error")+ifd(9,'"\', so it stayed there; renamed \'"','""')+ifd(9,"9.name",'""')+ifd(9,'"\'. The link still opens it."','""')
INARCH='{{if(contains(lower(11.body.name); "archive"); 11.body.name; if(contains(lower(12.body.name); "archive"); 12.body.name; if(contains(lower(13.body.name); "archive"); 13.body.name; if(contains(lower(14.body.name); "archive"); 14.body.name; ""))))}}'

flow=[
 {"id":99,"module":"gateway:CustomWebHook","version":1,"parameters":{"hook":HOOK,"maxResults":1},"mapper":{},"metadata":{"designer":{"x":0,"y":0}}},
 {"id":1,"module":"airtable:ActionSearchRecords","version":3,"parameters":{"__IMTCONN__":AT},
  "mapper":{"base":BASE,"table":TBL,"formulaField":"formula","maxRecords":50,"useColumnId":False,
   "formula":"AND({Clear out}!='', {Clear-out yes by}&''!='', {Clear-out yes on}, {Clear-out result}='', IF('{{99.record_id}}'='', TRUE(), RECORD_ID()='{{99.record_id}}'))"},
  "metadata":dz()},
 {"id":2,"module":"builtin:BasicRouter","version":1,"metadata":dz(),"routes":[
   {"flow":[dict(upd(10,"Refused "+D+": this link isn't a Drive file ("+LINK+"), so Make can't archive or trash it. Nothing was changed. If the page is already gone, this row can be cleared by hand."),
              filter=flt("Not a Drive file link",[[{"a":"{{1.id}}","o":"exist"},{"a":LINK,"o":"text:notpattern","b":PAT}]]))]},
   {"flow":[
     dict(drive(3,"/v3/files/"+FID,[("supportsAllDrives","true"),("fields",FF)],
        "Not done "+D+": Drive wouldn't open this file for the system login ({{#.error.message}}). Nothing was changed. The file may already be gone, or the system login may not have access to its drive."),
        filter=flt("Drive file link",[[{"a":"{{1.id}}","o":"exist"},{"a":LINK,"o":"text:pattern","b":PAT}]])),
     {"id":4,"module":"builtin:BasicRouter","version":1,"metadata":dz(),"routes":[
       {"flow":[dict(upd(40,"Nothing to do "+D+": the file was already in Drive's trash."),
          filter=flt("Already in trash",[[{"a":"{{3.body.trashed}}","o":"text:equal","b":"true"}]]))]},
       {"flow":[dict(call(5,"SCN_7193957",{"file_id":"{{3.body.id}}","confirm_name":"{{3.body.name}}"}),
          filter=flt("Delete, not yet trashed",[[{"a":"{{1.`Clear out`}}","o":"text:equal","b":"Delete"},{"a":"{{3.body.trashed}}","o":"text:notequal","b":"true"}]])),
          upd(6,trash_txt)]},
       {"flow":[dict(drive(11,"/v3/files/"+P[0],[("supportsAllDrives","true"),("fields","id,name,parents")],walkerr),
          filter=flt("Archive, not trashed",[[{"a":"{{1.`Clear out`}}","o":"text:equal","b":"Archive"},{"a":"{{3.body.trashed}}","o":"text:notequal","b":"true"}]])),
          drive(12,"/v3/files/"+P[1],[("supportsAllDrives","true"),("fields","id,name,parents")],walkerr),
          drive(13,"/v3/files/"+P[2],[("supportsAllDrives","true"),("fields","id,name,parents")],walkerr),
          drive(14,"/v3/files/"+P[3],[("supportsAllDrives","true"),("fields","id,name,parents")],walkerr),
          lst(21,P[0]),lst(22,P[1]),lst(23,P[2]),lst(24,P[3]),lst(25,P[4]),
          comp(33,INARCH),
          comp(26,pick("id")),comp(27,pick("name")),
          comp(30,'{{if(contains(3.body.mimeType; "application/vnd.google-apps"); "g"; if(contains(3.body.name; "."); "x"; "g"))}}'),
          comp(29,'Retired_{{if(30.value = "x"; substring(3.body.name; 0; length(3.body.name) - length(last(split(3.body.name; "."))) - 1); 3.body.name)}}_'+D+'{{if(30.value = "x"; "."; "")}}{{if(30.value = "x"; last(split(3.body.name; ".")); "")}}'),
          {"id":28,"module":"builtin:BasicRouter","version":1,"metadata":dz(),"routes":[
            {"flow":[dict(call(9,"SCN_7175763",{"file_id":"{{3.body.id}}","new_name":NEWNAME}),
               filter=flt("Already inside an archive folder",[[{"a":"{{33.value}}","o":"exist"}]])),
               upd(60,inarch_txt)]},
            {"flow":[dict(upd(50,"Refused "+D+": no folder named Archive was found above this file (looked five folders up). Nothing was changed."),
               filter=flt("No Archive folder",[[{"a":"{{33.value}}","o":"notexist"},{"a":"{{26.value}}","o":"notexist"}]]))]},
            {"flow":[dict(call(7,"SCN_7175763",{"file_id":"{{3.body.id}}","folder_id":"{{26.value}}","new_name":NEWNAME}),
               filter=flt("Archive folder found",[[{"a":"{{33.value}}","o":"notexist"},{"a":"{{26.value}}","o":"exist"}]])),
               upd(8,arch_txt)]}]}
       ]}
     ]}
   ]}
 ]}
]
bp={"name":"SAVVY 17 — Drive clear-out: Documents row ready (from Airtable) → SAVVY 15/16 → result back",
    "flow":flow,
    "metadata":{"version":1,"instant":True,"scenario":{"roundtrips":1,"maxErrors":3,"autoCommit":True,"autoCommitTriggerLast":True,"sequential":True,"confidential":False,"dataloss":False,"dlq":False,"freshVariables":False},"designer":{"orphans":[]}},
    "interface":{"input":[],"output":[]}}
json.dump(bp,open("savvy17_blueprint.json","w"),ensure_ascii=True)
print(len(json.dumps(bp)))
