(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_autoit"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/autoit.js":
/*!*************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/autoit.js ***!
  \*************************************************************************************************/
/***/ ((module) => {

/*
Language: AutoIt
Author: Manh Tuan <junookyo@gmail.com>
Description: AutoIt language definition
Category: scripting
*/

/** @type LanguageFn */
function autoit(hljs) {
  const KEYWORDS = 'ByRef Case Const ContinueCase ContinueLoop ' +
        'Dim Do Else ElseIf EndFunc EndIf EndSelect ' +
        'EndSwitch EndWith Enum Exit ExitLoop For Func ' +
        'Global If In Local Next ReDim Return Select Static ' +
        'Step Switch Then To Until Volatile WEnd While With';

  const DIRECTIVES = [
    "EndRegion",
    "forcedef",
    "forceref",
    "ignorefunc",
    "include",
    "include-once",
    "NoTrayIcon",
    "OnAutoItStartRegister",
    "pragma",
    "Region",
    "RequireAdmin",
    "Tidy_Off",
    "Tidy_On",
    "Tidy_Parameters"
  ];
  
  const LITERAL = 'True False And Null Not Or Default';

  const BUILT_IN
          = 'Abs ACos AdlibRegister AdlibUnRegister Asc AscW ASin Assign ATan AutoItSetOption AutoItWinGetTitle AutoItWinSetTitle Beep Binary BinaryLen BinaryMid BinaryToString BitAND BitNOT BitOR BitRotate BitShift BitXOR BlockInput Break Call CDTray Ceiling Chr ChrW ClipGet ClipPut ConsoleRead ConsoleWrite ConsoleWriteError ControlClick ControlCommand ControlDisable ControlEnable ControlFocus ControlGetFocus ControlGetHandle ControlGetPos ControlGetText ControlHide ControlListView ControlMove ControlSend ControlSetText ControlShow ControlTreeView Cos Dec DirCopy DirCreate DirGetSize DirMove DirRemove DllCall DllCallAddress DllCallbackFree DllCallbackGetPtr DllCallbackRegister DllClose DllOpen DllStructCreate DllStructGetData DllStructGetPtr DllStructGetSize DllStructSetData DriveGetDrive DriveGetFileSystem DriveGetLabel DriveGetSerial DriveGetType DriveMapAdd DriveMapDel DriveMapGet DriveSetLabel DriveSpaceFree DriveSpaceTotal DriveStatus EnvGet EnvSet EnvUpdate Eval Execute Exp FileChangeDir FileClose FileCopy FileCreateNTFSLink FileCreateShortcut FileDelete FileExists FileFindFirstFile FileFindNextFile FileFlush FileGetAttrib FileGetEncoding FileGetLongName FileGetPos FileGetShortcut FileGetShortName FileGetSize FileGetTime FileGetVersion FileInstall FileMove FileOpen FileOpenDialog FileRead FileReadLine FileReadToArray FileRecycle FileRecycleEmpty FileSaveDialog FileSelectFolder FileSetAttrib FileSetEnd FileSetPos FileSetTime FileWrite FileWriteLine Floor FtpSetProxy FuncName GUICreate GUICtrlCreateAvi GUICtrlCreateButton GUICtrlCreateCheckbox GUICtrlCreateCombo GUICtrlCreateContextMenu GUICtrlCreateDate GUICtrlCreateDummy GUICtrlCreateEdit GUICtrlCreateGraphic GUICtrlCreateGroup GUICtrlCreateIcon GUICtrlCreateInput GUICtrlCreateLabel GUICtrlCreateList GUICtrlCreateListView GUICtrlCreateListViewItem GUICtrlCreateMenu GUICtrlCreateMenuItem GUICtrlCreateMonthCal GUICtrlCreateObj GUICtrlCreatePic GUICtrlCreateProgress GUICtrlCreateRadio GUICtrlCreateSlider GUICtrlCreateTab GUICtrlCreateTabItem GUICtrlCreateTreeView GUICtrlCreateTreeViewItem GUICtrlCreateUpdown GUICtrlDelete GUICtrlGetHandle GUICtrlGetState GUICtrlRead GUICtrlRecvMsg GUICtrlRegisterListViewSort GUICtrlSendMsg GUICtrlSendToDummy GUICtrlSetBkColor GUICtrlSetColor GUICtrlSetCursor GUICtrlSetData GUICtrlSetDefBkColor GUICtrlSetDefColor GUICtrlSetFont GUICtrlSetGraphic GUICtrlSetImage GUICtrlSetLimit GUICtrlSetOnEvent GUICtrlSetPos GUICtrlSetResizing GUICtrlSetState GUICtrlSetStyle GUICtrlSetTip GUIDelete GUIGetCursorInfo GUIGetMsg GUIGetStyle GUIRegisterMsg GUISetAccelerators GUISetBkColor GUISetCoord GUISetCursor GUISetFont GUISetHelp GUISetIcon GUISetOnEvent GUISetState GUISetStyle GUIStartGroup GUISwitch Hex HotKeySet HttpSetProxy HttpSetUserAgent HWnd InetClose InetGet InetGetInfo InetGetSize InetRead IniDelete IniRead IniReadSection IniReadSectionNames IniRenameSection IniWrite IniWriteSection InputBox Int IsAdmin IsArray IsBinary IsBool IsDeclared IsDllStruct IsFloat IsFunc IsHWnd IsInt IsKeyword IsNumber IsObj IsPtr IsString Log MemGetStats Mod MouseClick MouseClickDrag MouseDown MouseGetCursor MouseGetPos MouseMove MouseUp MouseWheel MsgBox Number ObjCreate ObjCreateInterface ObjEvent ObjGet ObjName OnAutoItExitRegister OnAutoItExitUnRegister Ping PixelChecksum PixelGetColor PixelSearch ProcessClose ProcessExists ProcessGetStats ProcessList ProcessSetPriority ProcessWait ProcessWaitClose ProgressOff ProgressOn ProgressSet Ptr Random RegDelete RegEnumKey RegEnumVal RegRead RegWrite Round Run RunAs RunAsWait RunWait Send SendKeepActive SetError SetExtended ShellExecute ShellExecuteWait Shutdown Sin Sleep SoundPlay SoundSetWaveVolume SplashImageOn SplashOff SplashTextOn Sqrt SRandom StatusbarGetText StderrRead StdinWrite StdioClose StdoutRead String StringAddCR StringCompare StringFormat StringFromASCIIArray StringInStr StringIsAlNum StringIsAlpha StringIsASCII StringIsDigit StringIsFloat StringIsInt StringIsLower StringIsSpace StringIsUpper StringIsXDigit StringLeft StringLen StringLower StringMid StringRegExp StringRegExpReplace StringReplace StringReverse StringRight StringSplit StringStripCR StringStripWS StringToASCIIArray StringToBinary StringTrimLeft StringTrimRight StringUpper Tan TCPAccept TCPCloseSocket TCPConnect TCPListen TCPNameToIP TCPRecv TCPSend TCPShutdown, UDPShutdown TCPStartup, UDPStartup TimerDiff TimerInit ToolTip TrayCreateItem TrayCreateMenu TrayGetMsg TrayItemDelete TrayItemGetHandle TrayItemGetState TrayItemGetText TrayItemSetOnEvent TrayItemSetState TrayItemSetText TraySetClick TraySetIcon TraySetOnEvent TraySetPauseIcon TraySetState TraySetToolTip TrayTip UBound UDPBind UDPCloseSocket UDPOpen UDPRecv UDPSend VarGetType WinActivate WinActive WinClose WinExists WinFlash WinGetCaretPos WinGetClassList WinGetClientSize WinGetHandle WinGetPos WinGetProcess WinGetState WinGetText WinGetTitle WinKill WinList WinMenuSelectItem WinMinimizeAll WinMinimizeAllUndo WinMove WinSetOnTop WinSetState WinSetTitle WinSetTrans WinWait WinWaitActive WinWaitClose WinWaitNotActive';

  const COMMENT = {
    variants: [
      hljs.COMMENT(';', '$', {
        relevance: 0
      }),
      hljs.COMMENT('#cs', '#ce'),
      hljs.COMMENT('#comments-start', '#comments-end')
    ]
  };

  const VARIABLE = {
    begin: '\\$[A-z0-9_]+'
  };

  const STRING = {
    className: 'string',
    variants: [
      {
        begin: /"/,
        end: /"/,
        contains: [{
          begin: /""/,
          relevance: 0
        }]
      },
      {
        begin: /'/,
        end: /'/,
        contains: [{
          begin: /''/,
          relevance: 0
        }]
      }
    ]
  };

  const NUMBER = {
    variants: [
      hljs.BINARY_NUMBER_MODE,
      hljs.C_NUMBER_MODE
    ]
  };

  const PREPROCESSOR = {
    className: 'meta',
    begin: '#',
    end: '$',
    keywords: {
      'meta-keyword': DIRECTIVES
    },
    contains: [
      {
        begin: /\\\n/,
        relevance: 0
      },
      {
        beginKeywords: 'include',
        keywords: {
          'meta-keyword': 'include'
        },
        end: '$',
        contains: [
          STRING,
          {
            className: 'meta-string',
            variants: [
              {
                begin: '<',
                end: '>'
              },
              {
                begin: /"/,
                end: /"/,
                contains: [{
                  begin: /""/,
                  relevance: 0
                }]
              },
              {
                begin: /'/,
                end: /'/,
                contains: [{
                  begin: /''/,
                  relevance: 0
                }]
              }
            ]
          }
        ]
      },
      STRING,
      COMMENT
    ]
  };

  const CONSTANT = {
    className: 'symbol',
    // begin: '@',
    // end: '$',
    // keywords: 'AppDataCommonDir AppDataDir AutoItExe AutoItPID AutoItVersion AutoItX64 COM_EventObj CommonFilesDir Compiled ComputerName ComSpec CPUArch CR CRLF DesktopCommonDir DesktopDepth DesktopDir DesktopHeight DesktopRefresh DesktopWidth DocumentsCommonDir error exitCode exitMethod extended FavoritesCommonDir FavoritesDir GUI_CtrlHandle GUI_CtrlId GUI_DragFile GUI_DragId GUI_DropId GUI_WinHandle HomeDrive HomePath HomeShare HotKeyPressed HOUR IPAddress1 IPAddress2 IPAddress3 IPAddress4 KBLayout LF LocalAppDataDir LogonDNSDomain LogonDomain LogonServer MDAY MIN MON MSEC MUILang MyDocumentsDir NumParams OSArch OSBuild OSLang OSServicePack OSType OSVersion ProgramFilesDir ProgramsCommonDir ProgramsDir ScriptDir ScriptFullPath ScriptLineNumber ScriptName SEC StartMenuCommonDir StartMenuDir StartupCommonDir StartupDir SW_DISABLE SW_ENABLE SW_HIDE SW_LOCK SW_MAXIMIZE SW_MINIMIZE SW_RESTORE SW_SHOW SW_SHOWDEFAULT SW_SHOWMAXIMIZED SW_SHOWMINIMIZED SW_SHOWMINNOACTIVE SW_SHOWNA SW_SHOWNOACTIVATE SW_SHOWNORMAL SW_UNLOCK SystemDir TAB TempDir TRAY_ID TrayIconFlashing TrayIconVisible UserName UserProfileDir WDAY WindowsDir WorkingDir YDAY YEAR',
    // relevance: 5
    begin: '@[A-z0-9_]+'
  };

  const FUNCTION = {
    className: 'function',
    beginKeywords: 'Func',
    end: '$',
    illegal: '\\$|\\[|%',
    contains: [
      hljs.UNDERSCORE_TITLE_MODE,
      {
        className: 'params',
        begin: '\\(',
        end: '\\)',
        contains: [
          VARIABLE,
          STRING,
          NUMBER
        ]
      }
    ]
  };

  return {
    name: 'AutoIt',
    case_insensitive: true,
    illegal: /\/\*/,
    keywords: {
      keyword: KEYWORDS,
      built_in: BUILT_IN,
      literal: LITERAL
    },
    contains: [
      COMMENT,
      VARIABLE,
      STRING,
      NUMBER,
      PREPROCESSOR,
      CONSTANT,
      FUNCTION
    ]
  };
}

module.exports = autoit;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfYXV0b2l0LmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTs7QUFFQTtBQUNBO0FBQ0EscUJBQXFCO0FBQ3JCO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxTQUFTO0FBQ1QsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFNBQVM7QUFDVDtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBLFNBQVM7QUFDVDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxlQUFlO0FBQ2Y7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsaUJBQWlCO0FBQ2pCLGVBQWU7QUFDZjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxpQkFBaUI7QUFDakI7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL2F1dG9pdC5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuTGFuZ3VhZ2U6IEF1dG9JdFxuQXV0aG9yOiBNYW5oIFR1YW4gPGp1bm9va3lvQGdtYWlsLmNvbT5cbkRlc2NyaXB0aW9uOiBBdXRvSXQgbGFuZ3VhZ2UgZGVmaW5pdGlvblxuQ2F0ZWdvcnk6IHNjcmlwdGluZ1xuKi9cblxuLyoqIEB0eXBlIExhbmd1YWdlRm4gKi9cbmZ1bmN0aW9uIGF1dG9pdChobGpzKSB7XG4gIGNvbnN0IEtFWVdPUkRTID0gJ0J5UmVmIENhc2UgQ29uc3QgQ29udGludWVDYXNlIENvbnRpbnVlTG9vcCAnICtcbiAgICAgICAgJ0RpbSBEbyBFbHNlIEVsc2VJZiBFbmRGdW5jIEVuZElmIEVuZFNlbGVjdCAnICtcbiAgICAgICAgJ0VuZFN3aXRjaCBFbmRXaXRoIEVudW0gRXhpdCBFeGl0TG9vcCBGb3IgRnVuYyAnICtcbiAgICAgICAgJ0dsb2JhbCBJZiBJbiBMb2NhbCBOZXh0IFJlRGltIFJldHVybiBTZWxlY3QgU3RhdGljICcgK1xuICAgICAgICAnU3RlcCBTd2l0Y2ggVGhlbiBUbyBVbnRpbCBWb2xhdGlsZSBXRW5kIFdoaWxlIFdpdGgnO1xuXG4gIGNvbnN0IERJUkVDVElWRVMgPSBbXG4gICAgXCJFbmRSZWdpb25cIixcbiAgICBcImZvcmNlZGVmXCIsXG4gICAgXCJmb3JjZXJlZlwiLFxuICAgIFwiaWdub3JlZnVuY1wiLFxuICAgIFwiaW5jbHVkZVwiLFxuICAgIFwiaW5jbHVkZS1vbmNlXCIsXG4gICAgXCJOb1RyYXlJY29uXCIsXG4gICAgXCJPbkF1dG9JdFN0YXJ0UmVnaXN0ZXJcIixcbiAgICBcInByYWdtYVwiLFxuICAgIFwiUmVnaW9uXCIsXG4gICAgXCJSZXF1aXJlQWRtaW5cIixcbiAgICBcIlRpZHlfT2ZmXCIsXG4gICAgXCJUaWR5X09uXCIsXG4gICAgXCJUaWR5X1BhcmFtZXRlcnNcIlxuICBdO1xuICBcbiAgY29uc3QgTElURVJBTCA9ICdUcnVlIEZhbHNlIEFuZCBOdWxsIE5vdCBPciBEZWZhdWx0JztcblxuICBjb25zdCBCVUlMVF9JTlxuICAgICAgICAgID0gJ0FicyBBQ29zIEFkbGliUmVnaXN0ZXIgQWRsaWJVblJlZ2lzdGVyIEFzYyBBc2NXIEFTaW4gQXNzaWduIEFUYW4gQXV0b0l0U2V0T3B0aW9uIEF1dG9JdFdpbkdldFRpdGxlIEF1dG9JdFdpblNldFRpdGxlIEJlZXAgQmluYXJ5IEJpbmFyeUxlbiBCaW5hcnlNaWQgQmluYXJ5VG9TdHJpbmcgQml0QU5EIEJpdE5PVCBCaXRPUiBCaXRSb3RhdGUgQml0U2hpZnQgQml0WE9SIEJsb2NrSW5wdXQgQnJlYWsgQ2FsbCBDRFRyYXkgQ2VpbGluZyBDaHIgQ2hyVyBDbGlwR2V0IENsaXBQdXQgQ29uc29sZVJlYWQgQ29uc29sZVdyaXRlIENvbnNvbGVXcml0ZUVycm9yIENvbnRyb2xDbGljayBDb250cm9sQ29tbWFuZCBDb250cm9sRGlzYWJsZSBDb250cm9sRW5hYmxlIENvbnRyb2xGb2N1cyBDb250cm9sR2V0Rm9jdXMgQ29udHJvbEdldEhhbmRsZSBDb250cm9sR2V0UG9zIENvbnRyb2xHZXRUZXh0IENvbnRyb2xIaWRlIENvbnRyb2xMaXN0VmlldyBDb250cm9sTW92ZSBDb250cm9sU2VuZCBDb250cm9sU2V0VGV4dCBDb250cm9sU2hvdyBDb250cm9sVHJlZVZpZXcgQ29zIERlYyBEaXJDb3B5IERpckNyZWF0ZSBEaXJHZXRTaXplIERpck1vdmUgRGlyUmVtb3ZlIERsbENhbGwgRGxsQ2FsbEFkZHJlc3MgRGxsQ2FsbGJhY2tGcmVlIERsbENhbGxiYWNrR2V0UHRyIERsbENhbGxiYWNrUmVnaXN0ZXIgRGxsQ2xvc2UgRGxsT3BlbiBEbGxTdHJ1Y3RDcmVhdGUgRGxsU3RydWN0R2V0RGF0YSBEbGxTdHJ1Y3RHZXRQdHIgRGxsU3RydWN0R2V0U2l6ZSBEbGxTdHJ1Y3RTZXREYXRhIERyaXZlR2V0RHJpdmUgRHJpdmVHZXRGaWxlU3lzdGVtIERyaXZlR2V0TGFiZWwgRHJpdmVHZXRTZXJpYWwgRHJpdmVHZXRUeXBlIERyaXZlTWFwQWRkIERyaXZlTWFwRGVsIERyaXZlTWFwR2V0IERyaXZlU2V0TGFiZWwgRHJpdmVTcGFjZUZyZWUgRHJpdmVTcGFjZVRvdGFsIERyaXZlU3RhdHVzIEVudkdldCBFbnZTZXQgRW52VXBkYXRlIEV2YWwgRXhlY3V0ZSBFeHAgRmlsZUNoYW5nZURpciBGaWxlQ2xvc2UgRmlsZUNvcHkgRmlsZUNyZWF0ZU5URlNMaW5rIEZpbGVDcmVhdGVTaG9ydGN1dCBGaWxlRGVsZXRlIEZpbGVFeGlzdHMgRmlsZUZpbmRGaXJzdEZpbGUgRmlsZUZpbmROZXh0RmlsZSBGaWxlRmx1c2ggRmlsZUdldEF0dHJpYiBGaWxlR2V0RW5jb2RpbmcgRmlsZUdldExvbmdOYW1lIEZpbGVHZXRQb3MgRmlsZUdldFNob3J0Y3V0IEZpbGVHZXRTaG9ydE5hbWUgRmlsZUdldFNpemUgRmlsZUdldFRpbWUgRmlsZUdldFZlcnNpb24gRmlsZUluc3RhbGwgRmlsZU1vdmUgRmlsZU9wZW4gRmlsZU9wZW5EaWFsb2cgRmlsZVJlYWQgRmlsZVJlYWRMaW5lIEZpbGVSZWFkVG9BcnJheSBGaWxlUmVjeWNsZSBGaWxlUmVjeWNsZUVtcHR5IEZpbGVTYXZlRGlhbG9nIEZpbGVTZWxlY3RGb2xkZXIgRmlsZVNldEF0dHJpYiBGaWxlU2V0RW5kIEZpbGVTZXRQb3MgRmlsZVNldFRpbWUgRmlsZVdyaXRlIEZpbGVXcml0ZUxpbmUgRmxvb3IgRnRwU2V0UHJveHkgRnVuY05hbWUgR1VJQ3JlYXRlIEdVSUN0cmxDcmVhdGVBdmkgR1VJQ3RybENyZWF0ZUJ1dHRvbiBHVUlDdHJsQ3JlYXRlQ2hlY2tib3ggR1VJQ3RybENyZWF0ZUNvbWJvIEdVSUN0cmxDcmVhdGVDb250ZXh0TWVudSBHVUlDdHJsQ3JlYXRlRGF0ZSBHVUlDdHJsQ3JlYXRlRHVtbXkgR1VJQ3RybENyZWF0ZUVkaXQgR1VJQ3RybENyZWF0ZUdyYXBoaWMgR1VJQ3RybENyZWF0ZUdyb3VwIEdVSUN0cmxDcmVhdGVJY29uIEdVSUN0cmxDcmVhdGVJbnB1dCBHVUlDdHJsQ3JlYXRlTGFiZWwgR1VJQ3RybENyZWF0ZUxpc3QgR1VJQ3RybENyZWF0ZUxpc3RWaWV3IEdVSUN0cmxDcmVhdGVMaXN0Vmlld0l0ZW0gR1VJQ3RybENyZWF0ZU1lbnUgR1VJQ3RybENyZWF0ZU1lbnVJdGVtIEdVSUN0cmxDcmVhdGVNb250aENhbCBHVUlDdHJsQ3JlYXRlT2JqIEdVSUN0cmxDcmVhdGVQaWMgR1VJQ3RybENyZWF0ZVByb2dyZXNzIEdVSUN0cmxDcmVhdGVSYWRpbyBHVUlDdHJsQ3JlYXRlU2xpZGVyIEdVSUN0cmxDcmVhdGVUYWIgR1VJQ3RybENyZWF0ZVRhYkl0ZW0gR1VJQ3RybENyZWF0ZVRyZWVWaWV3IEdVSUN0cmxDcmVhdGVUcmVlVmlld0l0ZW0gR1VJQ3RybENyZWF0ZVVwZG93biBHVUlDdHJsRGVsZXRlIEdVSUN0cmxHZXRIYW5kbGUgR1VJQ3RybEdldFN0YXRlIEdVSUN0cmxSZWFkIEdVSUN0cmxSZWN2TXNnIEdVSUN0cmxSZWdpc3Rlckxpc3RWaWV3U29ydCBHVUlDdHJsU2VuZE1zZyBHVUlDdHJsU2VuZFRvRHVtbXkgR1VJQ3RybFNldEJrQ29sb3IgR1VJQ3RybFNldENvbG9yIEdVSUN0cmxTZXRDdXJzb3IgR1VJQ3RybFNldERhdGEgR1VJQ3RybFNldERlZkJrQ29sb3IgR1VJQ3RybFNldERlZkNvbG9yIEdVSUN0cmxTZXRGb250IEdVSUN0cmxTZXRHcmFwaGljIEdVSUN0cmxTZXRJbWFnZSBHVUlDdHJsU2V0TGltaXQgR1VJQ3RybFNldE9uRXZlbnQgR1VJQ3RybFNldFBvcyBHVUlDdHJsU2V0UmVzaXppbmcgR1VJQ3RybFNldFN0YXRlIEdVSUN0cmxTZXRTdHlsZSBHVUlDdHJsU2V0VGlwIEdVSURlbGV0ZSBHVUlHZXRDdXJzb3JJbmZvIEdVSUdldE1zZyBHVUlHZXRTdHlsZSBHVUlSZWdpc3Rlck1zZyBHVUlTZXRBY2NlbGVyYXRvcnMgR1VJU2V0QmtDb2xvciBHVUlTZXRDb29yZCBHVUlTZXRDdXJzb3IgR1VJU2V0Rm9udCBHVUlTZXRIZWxwIEdVSVNldEljb24gR1VJU2V0T25FdmVudCBHVUlTZXRTdGF0ZSBHVUlTZXRTdHlsZSBHVUlTdGFydEdyb3VwIEdVSVN3aXRjaCBIZXggSG90S2V5U2V0IEh0dHBTZXRQcm94eSBIdHRwU2V0VXNlckFnZW50IEhXbmQgSW5ldENsb3NlIEluZXRHZXQgSW5ldEdldEluZm8gSW5ldEdldFNpemUgSW5ldFJlYWQgSW5pRGVsZXRlIEluaVJlYWQgSW5pUmVhZFNlY3Rpb24gSW5pUmVhZFNlY3Rpb25OYW1lcyBJbmlSZW5hbWVTZWN0aW9uIEluaVdyaXRlIEluaVdyaXRlU2VjdGlvbiBJbnB1dEJveCBJbnQgSXNBZG1pbiBJc0FycmF5IElzQmluYXJ5IElzQm9vbCBJc0RlY2xhcmVkIElzRGxsU3RydWN0IElzRmxvYXQgSXNGdW5jIElzSFduZCBJc0ludCBJc0tleXdvcmQgSXNOdW1iZXIgSXNPYmogSXNQdHIgSXNTdHJpbmcgTG9nIE1lbUdldFN0YXRzIE1vZCBNb3VzZUNsaWNrIE1vdXNlQ2xpY2tEcmFnIE1vdXNlRG93biBNb3VzZUdldEN1cnNvciBNb3VzZUdldFBvcyBNb3VzZU1vdmUgTW91c2VVcCBNb3VzZVdoZWVsIE1zZ0JveCBOdW1iZXIgT2JqQ3JlYXRlIE9iakNyZWF0ZUludGVyZmFjZSBPYmpFdmVudCBPYmpHZXQgT2JqTmFtZSBPbkF1dG9JdEV4aXRSZWdpc3RlciBPbkF1dG9JdEV4aXRVblJlZ2lzdGVyIFBpbmcgUGl4ZWxDaGVja3N1bSBQaXhlbEdldENvbG9yIFBpeGVsU2VhcmNoIFByb2Nlc3NDbG9zZSBQcm9jZXNzRXhpc3RzIFByb2Nlc3NHZXRTdGF0cyBQcm9jZXNzTGlzdCBQcm9jZXNzU2V0UHJpb3JpdHkgUHJvY2Vzc1dhaXQgUHJvY2Vzc1dhaXRDbG9zZSBQcm9ncmVzc09mZiBQcm9ncmVzc09uIFByb2dyZXNzU2V0IFB0ciBSYW5kb20gUmVnRGVsZXRlIFJlZ0VudW1LZXkgUmVnRW51bVZhbCBSZWdSZWFkIFJlZ1dyaXRlIFJvdW5kIFJ1biBSdW5BcyBSdW5Bc1dhaXQgUnVuV2FpdCBTZW5kIFNlbmRLZWVwQWN0aXZlIFNldEVycm9yIFNldEV4dGVuZGVkIFNoZWxsRXhlY3V0ZSBTaGVsbEV4ZWN1dGVXYWl0IFNodXRkb3duIFNpbiBTbGVlcCBTb3VuZFBsYXkgU291bmRTZXRXYXZlVm9sdW1lIFNwbGFzaEltYWdlT24gU3BsYXNoT2ZmIFNwbGFzaFRleHRPbiBTcXJ0IFNSYW5kb20gU3RhdHVzYmFyR2V0VGV4dCBTdGRlcnJSZWFkIFN0ZGluV3JpdGUgU3RkaW9DbG9zZSBTdGRvdXRSZWFkIFN0cmluZyBTdHJpbmdBZGRDUiBTdHJpbmdDb21wYXJlIFN0cmluZ0Zvcm1hdCBTdHJpbmdGcm9tQVNDSUlBcnJheSBTdHJpbmdJblN0ciBTdHJpbmdJc0FsTnVtIFN0cmluZ0lzQWxwaGEgU3RyaW5nSXNBU0NJSSBTdHJpbmdJc0RpZ2l0IFN0cmluZ0lzRmxvYXQgU3RyaW5nSXNJbnQgU3RyaW5nSXNMb3dlciBTdHJpbmdJc1NwYWNlIFN0cmluZ0lzVXBwZXIgU3RyaW5nSXNYRGlnaXQgU3RyaW5nTGVmdCBTdHJpbmdMZW4gU3RyaW5nTG93ZXIgU3RyaW5nTWlkIFN0cmluZ1JlZ0V4cCBTdHJpbmdSZWdFeHBSZXBsYWNlIFN0cmluZ1JlcGxhY2UgU3RyaW5nUmV2ZXJzZSBTdHJpbmdSaWdodCBTdHJpbmdTcGxpdCBTdHJpbmdTdHJpcENSIFN0cmluZ1N0cmlwV1MgU3RyaW5nVG9BU0NJSUFycmF5IFN0cmluZ1RvQmluYXJ5IFN0cmluZ1RyaW1MZWZ0IFN0cmluZ1RyaW1SaWdodCBTdHJpbmdVcHBlciBUYW4gVENQQWNjZXB0IFRDUENsb3NlU29ja2V0IFRDUENvbm5lY3QgVENQTGlzdGVuIFRDUE5hbWVUb0lQIFRDUFJlY3YgVENQU2VuZCBUQ1BTaHV0ZG93biwgVURQU2h1dGRvd24gVENQU3RhcnR1cCwgVURQU3RhcnR1cCBUaW1lckRpZmYgVGltZXJJbml0IFRvb2xUaXAgVHJheUNyZWF0ZUl0ZW0gVHJheUNyZWF0ZU1lbnUgVHJheUdldE1zZyBUcmF5SXRlbURlbGV0ZSBUcmF5SXRlbUdldEhhbmRsZSBUcmF5SXRlbUdldFN0YXRlIFRyYXlJdGVtR2V0VGV4dCBUcmF5SXRlbVNldE9uRXZlbnQgVHJheUl0ZW1TZXRTdGF0ZSBUcmF5SXRlbVNldFRleHQgVHJheVNldENsaWNrIFRyYXlTZXRJY29uIFRyYXlTZXRPbkV2ZW50IFRyYXlTZXRQYXVzZUljb24gVHJheVNldFN0YXRlIFRyYXlTZXRUb29sVGlwIFRyYXlUaXAgVUJvdW5kIFVEUEJpbmQgVURQQ2xvc2VTb2NrZXQgVURQT3BlbiBVRFBSZWN2IFVEUFNlbmQgVmFyR2V0VHlwZSBXaW5BY3RpdmF0ZSBXaW5BY3RpdmUgV2luQ2xvc2UgV2luRXhpc3RzIFdpbkZsYXNoIFdpbkdldENhcmV0UG9zIFdpbkdldENsYXNzTGlzdCBXaW5HZXRDbGllbnRTaXplIFdpbkdldEhhbmRsZSBXaW5HZXRQb3MgV2luR2V0UHJvY2VzcyBXaW5HZXRTdGF0ZSBXaW5HZXRUZXh0IFdpbkdldFRpdGxlIFdpbktpbGwgV2luTGlzdCBXaW5NZW51U2VsZWN0SXRlbSBXaW5NaW5pbWl6ZUFsbCBXaW5NaW5pbWl6ZUFsbFVuZG8gV2luTW92ZSBXaW5TZXRPblRvcCBXaW5TZXRTdGF0ZSBXaW5TZXRUaXRsZSBXaW5TZXRUcmFucyBXaW5XYWl0IFdpbldhaXRBY3RpdmUgV2luV2FpdENsb3NlIFdpbldhaXROb3RBY3RpdmUnO1xuXG4gIGNvbnN0IENPTU1FTlQgPSB7XG4gICAgdmFyaWFudHM6IFtcbiAgICAgIGhsanMuQ09NTUVOVCgnOycsICckJywge1xuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH0pLFxuICAgICAgaGxqcy5DT01NRU5UKCcjY3MnLCAnI2NlJyksXG4gICAgICBobGpzLkNPTU1FTlQoJyNjb21tZW50cy1zdGFydCcsICcjY29tbWVudHMtZW5kJylcbiAgICBdXG4gIH07XG5cbiAgY29uc3QgVkFSSUFCTEUgPSB7XG4gICAgYmVnaW46ICdcXFxcJFtBLXowLTlfXSsnXG4gIH07XG5cbiAgY29uc3QgU1RSSU5HID0ge1xuICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgdmFyaWFudHM6IFtcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9cIi8sXG4gICAgICAgIGVuZDogL1wiLyxcbiAgICAgICAgY29udGFpbnM6IFt7XG4gICAgICAgICAgYmVnaW46IC9cIlwiLyxcbiAgICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgICAgfV1cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvJy8sXG4gICAgICAgIGVuZDogLycvLFxuICAgICAgICBjb250YWluczogW3tcbiAgICAgICAgICBiZWdpbjogLycnLyxcbiAgICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgICAgfV1cbiAgICAgIH1cbiAgICBdXG4gIH07XG5cbiAgY29uc3QgTlVNQkVSID0ge1xuICAgIHZhcmlhbnRzOiBbXG4gICAgICBobGpzLkJJTkFSWV9OVU1CRVJfTU9ERSxcbiAgICAgIGhsanMuQ19OVU1CRVJfTU9ERVxuICAgIF1cbiAgfTtcblxuICBjb25zdCBQUkVQUk9DRVNTT1IgPSB7XG4gICAgY2xhc3NOYW1lOiAnbWV0YScsXG4gICAgYmVnaW46ICcjJyxcbiAgICBlbmQ6ICckJyxcbiAgICBrZXl3b3Jkczoge1xuICAgICAgJ21ldGEta2V5d29yZCc6IERJUkVDVElWRVNcbiAgICB9LFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvXFxcXFxcbi8sXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW5LZXl3b3JkczogJ2luY2x1ZGUnLFxuICAgICAgICBrZXl3b3Jkczoge1xuICAgICAgICAgICdtZXRhLWtleXdvcmQnOiAnaW5jbHVkZSdcbiAgICAgICAgfSxcbiAgICAgICAgZW5kOiAnJCcsXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgU1RSSU5HLFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGNsYXNzTmFtZTogJ21ldGEtc3RyaW5nJyxcbiAgICAgICAgICAgIHZhcmlhbnRzOiBbXG4gICAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgICBiZWdpbjogJzwnLFxuICAgICAgICAgICAgICAgIGVuZDogJz4nXG4gICAgICAgICAgICAgIH0sXG4gICAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgICBiZWdpbjogL1wiLyxcbiAgICAgICAgICAgICAgICBlbmQ6IC9cIi8sXG4gICAgICAgICAgICAgICAgY29udGFpbnM6IFt7XG4gICAgICAgICAgICAgICAgICBiZWdpbjogL1wiXCIvLFxuICAgICAgICAgICAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICAgICAgICAgICAgfV1cbiAgICAgICAgICAgICAgfSxcbiAgICAgICAgICAgICAge1xuICAgICAgICAgICAgICAgIGJlZ2luOiAvJy8sXG4gICAgICAgICAgICAgICAgZW5kOiAvJy8sXG4gICAgICAgICAgICAgICAgY29udGFpbnM6IFt7XG4gICAgICAgICAgICAgICAgICBiZWdpbjogLycnLyxcbiAgICAgICAgICAgICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgICAgICAgICAgIH1dXG4gICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIF1cbiAgICAgICAgICB9XG4gICAgICAgIF1cbiAgICAgIH0sXG4gICAgICBTVFJJTkcsXG4gICAgICBDT01NRU5UXG4gICAgXVxuICB9O1xuXG4gIGNvbnN0IENPTlNUQU5UID0ge1xuICAgIGNsYXNzTmFtZTogJ3N5bWJvbCcsXG4gICAgLy8gYmVnaW46ICdAJyxcbiAgICAvLyBlbmQ6ICckJyxcbiAgICAvLyBrZXl3b3JkczogJ0FwcERhdGFDb21tb25EaXIgQXBwRGF0YURpciBBdXRvSXRFeGUgQXV0b0l0UElEIEF1dG9JdFZlcnNpb24gQXV0b0l0WDY0IENPTV9FdmVudE9iaiBDb21tb25GaWxlc0RpciBDb21waWxlZCBDb21wdXRlck5hbWUgQ29tU3BlYyBDUFVBcmNoIENSIENSTEYgRGVza3RvcENvbW1vbkRpciBEZXNrdG9wRGVwdGggRGVza3RvcERpciBEZXNrdG9wSGVpZ2h0IERlc2t0b3BSZWZyZXNoIERlc2t0b3BXaWR0aCBEb2N1bWVudHNDb21tb25EaXIgZXJyb3IgZXhpdENvZGUgZXhpdE1ldGhvZCBleHRlbmRlZCBGYXZvcml0ZXNDb21tb25EaXIgRmF2b3JpdGVzRGlyIEdVSV9DdHJsSGFuZGxlIEdVSV9DdHJsSWQgR1VJX0RyYWdGaWxlIEdVSV9EcmFnSWQgR1VJX0Ryb3BJZCBHVUlfV2luSGFuZGxlIEhvbWVEcml2ZSBIb21lUGF0aCBIb21lU2hhcmUgSG90S2V5UHJlc3NlZCBIT1VSIElQQWRkcmVzczEgSVBBZGRyZXNzMiBJUEFkZHJlc3MzIElQQWRkcmVzczQgS0JMYXlvdXQgTEYgTG9jYWxBcHBEYXRhRGlyIExvZ29uRE5TRG9tYWluIExvZ29uRG9tYWluIExvZ29uU2VydmVyIE1EQVkgTUlOIE1PTiBNU0VDIE1VSUxhbmcgTXlEb2N1bWVudHNEaXIgTnVtUGFyYW1zIE9TQXJjaCBPU0J1aWxkIE9TTGFuZyBPU1NlcnZpY2VQYWNrIE9TVHlwZSBPU1ZlcnNpb24gUHJvZ3JhbUZpbGVzRGlyIFByb2dyYW1zQ29tbW9uRGlyIFByb2dyYW1zRGlyIFNjcmlwdERpciBTY3JpcHRGdWxsUGF0aCBTY3JpcHRMaW5lTnVtYmVyIFNjcmlwdE5hbWUgU0VDIFN0YXJ0TWVudUNvbW1vbkRpciBTdGFydE1lbnVEaXIgU3RhcnR1cENvbW1vbkRpciBTdGFydHVwRGlyIFNXX0RJU0FCTEUgU1dfRU5BQkxFIFNXX0hJREUgU1dfTE9DSyBTV19NQVhJTUlaRSBTV19NSU5JTUlaRSBTV19SRVNUT1JFIFNXX1NIT1cgU1dfU0hPV0RFRkFVTFQgU1dfU0hPV01BWElNSVpFRCBTV19TSE9XTUlOSU1JWkVEIFNXX1NIT1dNSU5OT0FDVElWRSBTV19TSE9XTkEgU1dfU0hPV05PQUNUSVZBVEUgU1dfU0hPV05PUk1BTCBTV19VTkxPQ0sgU3lzdGVtRGlyIFRBQiBUZW1wRGlyIFRSQVlfSUQgVHJheUljb25GbGFzaGluZyBUcmF5SWNvblZpc2libGUgVXNlck5hbWUgVXNlclByb2ZpbGVEaXIgV0RBWSBXaW5kb3dzRGlyIFdvcmtpbmdEaXIgWURBWSBZRUFSJyxcbiAgICAvLyByZWxldmFuY2U6IDVcbiAgICBiZWdpbjogJ0BbQS16MC05X10rJ1xuICB9O1xuXG4gIGNvbnN0IEZVTkNUSU9OID0ge1xuICAgIGNsYXNzTmFtZTogJ2Z1bmN0aW9uJyxcbiAgICBiZWdpbktleXdvcmRzOiAnRnVuYycsXG4gICAgZW5kOiAnJCcsXG4gICAgaWxsZWdhbDogJ1xcXFwkfFxcXFxbfCUnLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBobGpzLlVOREVSU0NPUkVfVElUTEVfTU9ERSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAncGFyYW1zJyxcbiAgICAgICAgYmVnaW46ICdcXFxcKCcsXG4gICAgICAgIGVuZDogJ1xcXFwpJyxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICBWQVJJQUJMRSxcbiAgICAgICAgICBTVFJJTkcsXG4gICAgICAgICAgTlVNQkVSXG4gICAgICAgIF1cbiAgICAgIH1cbiAgICBdXG4gIH07XG5cbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnQXV0b0l0JyxcbiAgICBjYXNlX2luc2Vuc2l0aXZlOiB0cnVlLFxuICAgIGlsbGVnYWw6IC9cXC9cXCovLFxuICAgIGtleXdvcmRzOiB7XG4gICAgICBrZXl3b3JkOiBLRVlXT1JEUyxcbiAgICAgIGJ1aWx0X2luOiBCVUlMVF9JTixcbiAgICAgIGxpdGVyYWw6IExJVEVSQUxcbiAgICB9LFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBDT01NRU5ULFxuICAgICAgVkFSSUFCTEUsXG4gICAgICBTVFJJTkcsXG4gICAgICBOVU1CRVIsXG4gICAgICBQUkVQUk9DRVNTT1IsXG4gICAgICBDT05TVEFOVCxcbiAgICAgIEZVTkNUSU9OXG4gICAgXVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IGF1dG9pdDtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==