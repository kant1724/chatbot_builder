var MinVersion = 0x0505010C;
var data;
var pHwpCtrl;

$(document).ready(function() {
	var title = $('#title').val();
	pHwpCtrl = document.HwpCtrl;
	var root = "http://" + $('#file_ip').val() + "/";
    var addr = root + "static/hwp/recommend_fund.hwp?timestamp=" + new Date().getTime();
	pHwpCtrl.open(addr);
    //document.HwpCtrl.SetClientName("DEBUG");
    //URLOpen();
});

function _VerifyVersion() {
    // 설치확인
    if(pHwpCtrl.getAttribute("Version") == null) {
        alert("한글 2002 컨트롤이 설치되지 않았습니다.");
        return;
    }
    //버젼 확인
    CurVersion = pHwpCtrl.Version;
    alert(pHwpCtrl.getAttribute("Version"))
    alert(CurVersion.toString(16));
    if(CurVersion < MinVersion) {
        alert(!"HwpCtrl의 버젼이 낮아서 정상적으로 동작하지 않을 수 있습니다.\n"+"최신 버젼으로 업데이트하기를 권장합니다.\n\n"
              + "현재 버젼: 0x"
              + CurVersion.toString(16)
              + "\n"
              + "권장 버젼: 0x"
              + MinVersion.toString(16) + " 이상");
    }
}

function URLOpen() {
    var bRes = document.HwpCtrl.RegisterModule("FilePathCheckDLL", "FilePathChecker");
    document.HwpCtrl.Clear(1);
    
    document.HwpCtrl.Open(addr)
    document.HwpCtrl.EditMode=1;
    document.HwpCtrl.MovePos(2);
}
