(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_nsis"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/nsis.js":
/*!***********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/nsis.js ***!
  \***********************************************************************************************/
/***/ ((module) => {

/*
Language: NSIS
Description: Nullsoft Scriptable Install System
Author: Jan T. Sott <jan.sott@gmail.com>
Website: https://nsis.sourceforge.io/Main_Page
*/

function nsis(hljs) {
  const CONSTANTS = {
    className: 'variable',
    begin: /\$(ADMINTOOLS|APPDATA|CDBURN_AREA|CMDLINE|COMMONFILES32|COMMONFILES64|COMMONFILES|COOKIES|DESKTOP|DOCUMENTS|EXEDIR|EXEFILE|EXEPATH|FAVORITES|FONTS|HISTORY|HWNDPARENT|INSTDIR|INTERNET_CACHE|LANGUAGE|LOCALAPPDATA|MUSIC|NETHOOD|OUTDIR|PICTURES|PLUGINSDIR|PRINTHOOD|PROFILE|PROGRAMFILES32|PROGRAMFILES64|PROGRAMFILES|QUICKLAUNCH|RECENT|RESOURCES_LOCALIZED|RESOURCES|SENDTO|SMPROGRAMS|SMSTARTUP|STARTMENU|SYSDIR|TEMP|TEMPLATES|VIDEOS|WINDIR)/
  };

  const DEFINES = {
    // ${defines}
    className: 'variable',
    begin: /\$+\{[\w.:-]+\}/
  };

  const VARIABLES = {
    // $variables
    className: 'variable',
    begin: /\$+\w+/,
    illegal: /\(\)\{\}/
  };

  const LANGUAGES = {
    // $(language_strings)
    className: 'variable',
    begin: /\$+\([\w^.:-]+\)/
  };

  const PARAMETERS = {
    // command parameters
    className: 'params',
    begin: '(ARCHIVE|FILE_ATTRIBUTE_ARCHIVE|FILE_ATTRIBUTE_NORMAL|FILE_ATTRIBUTE_OFFLINE|FILE_ATTRIBUTE_READONLY|FILE_ATTRIBUTE_SYSTEM|FILE_ATTRIBUTE_TEMPORARY|HKCR|HKCU|HKDD|HKEY_CLASSES_ROOT|HKEY_CURRENT_CONFIG|HKEY_CURRENT_USER|HKEY_DYN_DATA|HKEY_LOCAL_MACHINE|HKEY_PERFORMANCE_DATA|HKEY_USERS|HKLM|HKPD|HKU|IDABORT|IDCANCEL|IDIGNORE|IDNO|IDOK|IDRETRY|IDYES|MB_ABORTRETRYIGNORE|MB_DEFBUTTON1|MB_DEFBUTTON2|MB_DEFBUTTON3|MB_DEFBUTTON4|MB_ICONEXCLAMATION|MB_ICONINFORMATION|MB_ICONQUESTION|MB_ICONSTOP|MB_OK|MB_OKCANCEL|MB_RETRYCANCEL|MB_RIGHT|MB_RTLREADING|MB_SETFOREGROUND|MB_TOPMOST|MB_USERICON|MB_YESNO|NORMAL|OFFLINE|READONLY|SHCTX|SHELL_CONTEXT|SYSTEM|TEMPORARY)'
  };

  const COMPILER = {
    // !compiler_flags
    className: 'keyword',
    begin: /!(addincludedir|addplugindir|appendfile|cd|define|delfile|echo|else|endif|error|execute|finalize|getdllversion|gettlbversion|if|ifdef|ifmacrodef|ifmacrondef|ifndef|include|insertmacro|macro|macroend|makensis|packhdr|searchparse|searchreplace|system|tempfile|undef|verbose|warning)/
  };

  const METACHARS = {
    // $\n, $\r, $\t, $$
    className: 'meta',
    begin: /\$(\\[nrt]|\$)/
  };

  const PLUGINS = {
    // plug::ins
    className: 'class',
    begin: /\w+::\w+/
  };

  const STRING = {
    className: 'string',
    variants: [
      {
        begin: '"',
        end: '"'
      },
      {
        begin: '\'',
        end: '\''
      },
      {
        begin: '`',
        end: '`'
      }
    ],
    illegal: /\n/,
    contains: [
      METACHARS,
      CONSTANTS,
      DEFINES,
      VARIABLES,
      LANGUAGES
    ]
  };

  return {
    name: 'NSIS',
    case_insensitive: false,
    keywords: {
      keyword:
      'Abort AddBrandingImage AddSize AllowRootDirInstall AllowSkipFiles AutoCloseWindow BGFont BGGradient BrandingText BringToFront Call CallInstDLL Caption ChangeUI CheckBitmap ClearErrors CompletedText ComponentText CopyFiles CRCCheck CreateDirectory CreateFont CreateShortCut Delete DeleteINISec DeleteINIStr DeleteRegKey DeleteRegValue DetailPrint DetailsButtonText DirText DirVar DirVerify EnableWindow EnumRegKey EnumRegValue Exch Exec ExecShell ExecShellWait ExecWait ExpandEnvStrings File FileBufSize FileClose FileErrorText FileOpen FileRead FileReadByte FileReadUTF16LE FileReadWord FileWriteUTF16LE FileSeek FileWrite FileWriteByte FileWriteWord FindClose FindFirst FindNext FindWindow FlushINI GetCurInstType GetCurrentAddress GetDlgItem GetDLLVersion GetDLLVersionLocal GetErrorLevel GetFileTime GetFileTimeLocal GetFullPathName GetFunctionAddress GetInstDirError GetKnownFolderPath GetLabelAddress GetTempFileName Goto HideWindow Icon IfAbort IfErrors IfFileExists IfRebootFlag IfRtlLanguage IfShellVarContextAll IfSilent InitPluginsDir InstallButtonText InstallColors InstallDir InstallDirRegKey InstProgressFlags InstType InstTypeGetText InstTypeSetText Int64Cmp Int64CmpU Int64Fmt IntCmp IntCmpU IntFmt IntOp IntPtrCmp IntPtrCmpU IntPtrOp IsWindow LangString LicenseBkColor LicenseData LicenseForceSelection LicenseLangString LicenseText LoadAndSetImage LoadLanguageFile LockWindow LogSet LogText ManifestDPIAware ManifestLongPathAware ManifestMaxVersionTested ManifestSupportedOS MessageBox MiscButtonText Name Nop OutFile Page PageCallbacks PEAddResource PEDllCharacteristics PERemoveResource PESubsysVer Pop Push Quit ReadEnvStr ReadINIStr ReadRegDWORD ReadRegStr Reboot RegDLL Rename RequestExecutionLevel ReserveFile Return RMDir SearchPath SectionGetFlags SectionGetInstTypes SectionGetSize SectionGetText SectionIn SectionSetFlags SectionSetInstTypes SectionSetSize SectionSetText SendMessage SetAutoClose SetBrandingImage SetCompress SetCompressor SetCompressorDictSize SetCtlColors SetCurInstType SetDatablockOptimize SetDateSave SetDetailsPrint SetDetailsView SetErrorLevel SetErrors SetFileAttributes SetFont SetOutPath SetOverwrite SetRebootFlag SetRegView SetShellVarContext SetSilent ShowInstDetails ShowUninstDetails ShowWindow SilentInstall SilentUnInstall Sleep SpaceTexts StrCmp StrCmpS StrCpy StrLen SubCaption Unicode UninstallButtonText UninstallCaption UninstallIcon UninstallSubCaption UninstallText UninstPage UnRegDLL Var VIAddVersionKey VIFileVersion VIProductVersion WindowIcon WriteINIStr WriteRegBin WriteRegDWORD WriteRegExpandStr WriteRegMultiStr WriteRegNone WriteRegStr WriteUninstaller XPStyle',
      literal:
      'admin all auto both bottom bzip2 colored components current custom directory false force hide highest ifdiff ifnewer instfiles lastused leave left license listonly lzma nevershow none normal notset off on open print right show silent silentlog smooth textonly top true try un.components un.custom un.directory un.instfiles un.license uninstConfirm user Win10 Win7 Win8 WinVista zlib'
    },
    contains: [
      hljs.HASH_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE,
      hljs.COMMENT(
        ';',
        '$',
        {
          relevance: 0
        }
      ),
      {
        className: 'function',
        beginKeywords: 'Function PageEx Section SectionGroup',
        end: '$'
      },
      STRING,
      COMPILER,
      DEFINES,
      VARIABLES,
      LANGUAGES,
      PARAMETERS,
      PLUGINS,
      hljs.NUMBER_MODE
    ]
  };
}

module.exports = nsis;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfbnNpcy5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBLFNBQVM7QUFDVDtBQUNBLGlCQUFpQixVQUFVO0FBQzNCOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0Esb0JBQW9CLEVBQUU7QUFDdEI7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsVUFBVTtBQUNWO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9uc2lzLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogTlNJU1xuRGVzY3JpcHRpb246IE51bGxzb2Z0IFNjcmlwdGFibGUgSW5zdGFsbCBTeXN0ZW1cbkF1dGhvcjogSmFuIFQuIFNvdHQgPGphbi5zb3R0QGdtYWlsLmNvbT5cbldlYnNpdGU6IGh0dHBzOi8vbnNpcy5zb3VyY2Vmb3JnZS5pby9NYWluX1BhZ2VcbiovXG5cbmZ1bmN0aW9uIG5zaXMoaGxqcykge1xuICBjb25zdCBDT05TVEFOVFMgPSB7XG4gICAgY2xhc3NOYW1lOiAndmFyaWFibGUnLFxuICAgIGJlZ2luOiAvXFwkKEFETUlOVE9PTFN8QVBQREFUQXxDREJVUk5fQVJFQXxDTURMSU5FfENPTU1PTkZJTEVTMzJ8Q09NTU9ORklMRVM2NHxDT01NT05GSUxFU3xDT09LSUVTfERFU0tUT1B8RE9DVU1FTlRTfEVYRURJUnxFWEVGSUxFfEVYRVBBVEh8RkFWT1JJVEVTfEZPTlRTfEhJU1RPUll8SFdORFBBUkVOVHxJTlNURElSfElOVEVSTkVUX0NBQ0hFfExBTkdVQUdFfExPQ0FMQVBQREFUQXxNVVNJQ3xORVRIT09EfE9VVERJUnxQSUNUVVJFU3xQTFVHSU5TRElSfFBSSU5USE9PRHxQUk9GSUxFfFBST0dSQU1GSUxFUzMyfFBST0dSQU1GSUxFUzY0fFBST0dSQU1GSUxFU3xRVUlDS0xBVU5DSHxSRUNFTlR8UkVTT1VSQ0VTX0xPQ0FMSVpFRHxSRVNPVVJDRVN8U0VORFRPfFNNUFJPR1JBTVN8U01TVEFSVFVQfFNUQVJUTUVOVXxTWVNESVJ8VEVNUHxURU1QTEFURVN8VklERU9TfFdJTkRJUikvXG4gIH07XG5cbiAgY29uc3QgREVGSU5FUyA9IHtcbiAgICAvLyAke2RlZmluZXN9XG4gICAgY2xhc3NOYW1lOiAndmFyaWFibGUnLFxuICAgIGJlZ2luOiAvXFwkK1xce1tcXHcuOi1dK1xcfS9cbiAgfTtcblxuICBjb25zdCBWQVJJQUJMRVMgPSB7XG4gICAgLy8gJHZhcmlhYmxlc1xuICAgIGNsYXNzTmFtZTogJ3ZhcmlhYmxlJyxcbiAgICBiZWdpbjogL1xcJCtcXHcrLyxcbiAgICBpbGxlZ2FsOiAvXFwoXFwpXFx7XFx9L1xuICB9O1xuXG4gIGNvbnN0IExBTkdVQUdFUyA9IHtcbiAgICAvLyAkKGxhbmd1YWdlX3N0cmluZ3MpXG4gICAgY2xhc3NOYW1lOiAndmFyaWFibGUnLFxuICAgIGJlZ2luOiAvXFwkK1xcKFtcXHdeLjotXStcXCkvXG4gIH07XG5cbiAgY29uc3QgUEFSQU1FVEVSUyA9IHtcbiAgICAvLyBjb21tYW5kIHBhcmFtZXRlcnNcbiAgICBjbGFzc05hbWU6ICdwYXJhbXMnLFxuICAgIGJlZ2luOiAnKEFSQ0hJVkV8RklMRV9BVFRSSUJVVEVfQVJDSElWRXxGSUxFX0FUVFJJQlVURV9OT1JNQUx8RklMRV9BVFRSSUJVVEVfT0ZGTElORXxGSUxFX0FUVFJJQlVURV9SRUFET05MWXxGSUxFX0FUVFJJQlVURV9TWVNURU18RklMRV9BVFRSSUJVVEVfVEVNUE9SQVJZfEhLQ1J8SEtDVXxIS0REfEhLRVlfQ0xBU1NFU19ST09UfEhLRVlfQ1VSUkVOVF9DT05GSUd8SEtFWV9DVVJSRU5UX1VTRVJ8SEtFWV9EWU5fREFUQXxIS0VZX0xPQ0FMX01BQ0hJTkV8SEtFWV9QRVJGT1JNQU5DRV9EQVRBfEhLRVlfVVNFUlN8SEtMTXxIS1BEfEhLVXxJREFCT1JUfElEQ0FOQ0VMfElESUdOT1JFfElETk98SURPS3xJRFJFVFJZfElEWUVTfE1CX0FCT1JUUkVUUllJR05PUkV8TUJfREVGQlVUVE9OMXxNQl9ERUZCVVRUT04yfE1CX0RFRkJVVFRPTjN8TUJfREVGQlVUVE9ONHxNQl9JQ09ORVhDTEFNQVRJT058TUJfSUNPTklORk9STUFUSU9OfE1CX0lDT05RVUVTVElPTnxNQl9JQ09OU1RPUHxNQl9PS3xNQl9PS0NBTkNFTHxNQl9SRVRSWUNBTkNFTHxNQl9SSUdIVHxNQl9SVExSRUFESU5HfE1CX1NFVEZPUkVHUk9VTkR8TUJfVE9QTU9TVHxNQl9VU0VSSUNPTnxNQl9ZRVNOT3xOT1JNQUx8T0ZGTElORXxSRUFET05MWXxTSENUWHxTSEVMTF9DT05URVhUfFNZU1RFTXxURU1QT1JBUlkpJ1xuICB9O1xuXG4gIGNvbnN0IENPTVBJTEVSID0ge1xuICAgIC8vICFjb21waWxlcl9mbGFnc1xuICAgIGNsYXNzTmFtZTogJ2tleXdvcmQnLFxuICAgIGJlZ2luOiAvIShhZGRpbmNsdWRlZGlyfGFkZHBsdWdpbmRpcnxhcHBlbmRmaWxlfGNkfGRlZmluZXxkZWxmaWxlfGVjaG98ZWxzZXxlbmRpZnxlcnJvcnxleGVjdXRlfGZpbmFsaXplfGdldGRsbHZlcnNpb258Z2V0dGxidmVyc2lvbnxpZnxpZmRlZnxpZm1hY3JvZGVmfGlmbWFjcm9uZGVmfGlmbmRlZnxpbmNsdWRlfGluc2VydG1hY3JvfG1hY3JvfG1hY3JvZW5kfG1ha2Vuc2lzfHBhY2toZHJ8c2VhcmNocGFyc2V8c2VhcmNocmVwbGFjZXxzeXN0ZW18dGVtcGZpbGV8dW5kZWZ8dmVyYm9zZXx3YXJuaW5nKS9cbiAgfTtcblxuICBjb25zdCBNRVRBQ0hBUlMgPSB7XG4gICAgLy8gJFxcbiwgJFxcciwgJFxcdCwgJCRcbiAgICBjbGFzc05hbWU6ICdtZXRhJyxcbiAgICBiZWdpbjogL1xcJChcXFxcW25ydF18XFwkKS9cbiAgfTtcblxuICBjb25zdCBQTFVHSU5TID0ge1xuICAgIC8vIHBsdWc6Omluc1xuICAgIGNsYXNzTmFtZTogJ2NsYXNzJyxcbiAgICBiZWdpbjogL1xcdys6OlxcdysvXG4gIH07XG5cbiAgY29uc3QgU1RSSU5HID0ge1xuICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgdmFyaWFudHM6IFtcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICdcIicsXG4gICAgICAgIGVuZDogJ1wiJ1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICdcXCcnLFxuICAgICAgICBlbmQ6ICdcXCcnXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogJ2AnLFxuICAgICAgICBlbmQ6ICdgJ1xuICAgICAgfVxuICAgIF0sXG4gICAgaWxsZWdhbDogL1xcbi8sXG4gICAgY29udGFpbnM6IFtcbiAgICAgIE1FVEFDSEFSUyxcbiAgICAgIENPTlNUQU5UUyxcbiAgICAgIERFRklORVMsXG4gICAgICBWQVJJQUJMRVMsXG4gICAgICBMQU5HVUFHRVNcbiAgICBdXG4gIH07XG5cbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnTlNJUycsXG4gICAgY2FzZV9pbnNlbnNpdGl2ZTogZmFsc2UsXG4gICAga2V5d29yZHM6IHtcbiAgICAgIGtleXdvcmQ6XG4gICAgICAnQWJvcnQgQWRkQnJhbmRpbmdJbWFnZSBBZGRTaXplIEFsbG93Um9vdERpckluc3RhbGwgQWxsb3dTa2lwRmlsZXMgQXV0b0Nsb3NlV2luZG93IEJHRm9udCBCR0dyYWRpZW50IEJyYW5kaW5nVGV4dCBCcmluZ1RvRnJvbnQgQ2FsbCBDYWxsSW5zdERMTCBDYXB0aW9uIENoYW5nZVVJIENoZWNrQml0bWFwIENsZWFyRXJyb3JzIENvbXBsZXRlZFRleHQgQ29tcG9uZW50VGV4dCBDb3B5RmlsZXMgQ1JDQ2hlY2sgQ3JlYXRlRGlyZWN0b3J5IENyZWF0ZUZvbnQgQ3JlYXRlU2hvcnRDdXQgRGVsZXRlIERlbGV0ZUlOSVNlYyBEZWxldGVJTklTdHIgRGVsZXRlUmVnS2V5IERlbGV0ZVJlZ1ZhbHVlIERldGFpbFByaW50IERldGFpbHNCdXR0b25UZXh0IERpclRleHQgRGlyVmFyIERpclZlcmlmeSBFbmFibGVXaW5kb3cgRW51bVJlZ0tleSBFbnVtUmVnVmFsdWUgRXhjaCBFeGVjIEV4ZWNTaGVsbCBFeGVjU2hlbGxXYWl0IEV4ZWNXYWl0IEV4cGFuZEVudlN0cmluZ3MgRmlsZSBGaWxlQnVmU2l6ZSBGaWxlQ2xvc2UgRmlsZUVycm9yVGV4dCBGaWxlT3BlbiBGaWxlUmVhZCBGaWxlUmVhZEJ5dGUgRmlsZVJlYWRVVEYxNkxFIEZpbGVSZWFkV29yZCBGaWxlV3JpdGVVVEYxNkxFIEZpbGVTZWVrIEZpbGVXcml0ZSBGaWxlV3JpdGVCeXRlIEZpbGVXcml0ZVdvcmQgRmluZENsb3NlIEZpbmRGaXJzdCBGaW5kTmV4dCBGaW5kV2luZG93IEZsdXNoSU5JIEdldEN1ckluc3RUeXBlIEdldEN1cnJlbnRBZGRyZXNzIEdldERsZ0l0ZW0gR2V0RExMVmVyc2lvbiBHZXRETExWZXJzaW9uTG9jYWwgR2V0RXJyb3JMZXZlbCBHZXRGaWxlVGltZSBHZXRGaWxlVGltZUxvY2FsIEdldEZ1bGxQYXRoTmFtZSBHZXRGdW5jdGlvbkFkZHJlc3MgR2V0SW5zdERpckVycm9yIEdldEtub3duRm9sZGVyUGF0aCBHZXRMYWJlbEFkZHJlc3MgR2V0VGVtcEZpbGVOYW1lIEdvdG8gSGlkZVdpbmRvdyBJY29uIElmQWJvcnQgSWZFcnJvcnMgSWZGaWxlRXhpc3RzIElmUmVib290RmxhZyBJZlJ0bExhbmd1YWdlIElmU2hlbGxWYXJDb250ZXh0QWxsIElmU2lsZW50IEluaXRQbHVnaW5zRGlyIEluc3RhbGxCdXR0b25UZXh0IEluc3RhbGxDb2xvcnMgSW5zdGFsbERpciBJbnN0YWxsRGlyUmVnS2V5IEluc3RQcm9ncmVzc0ZsYWdzIEluc3RUeXBlIEluc3RUeXBlR2V0VGV4dCBJbnN0VHlwZVNldFRleHQgSW50NjRDbXAgSW50NjRDbXBVIEludDY0Rm10IEludENtcCBJbnRDbXBVIEludEZtdCBJbnRPcCBJbnRQdHJDbXAgSW50UHRyQ21wVSBJbnRQdHJPcCBJc1dpbmRvdyBMYW5nU3RyaW5nIExpY2Vuc2VCa0NvbG9yIExpY2Vuc2VEYXRhIExpY2Vuc2VGb3JjZVNlbGVjdGlvbiBMaWNlbnNlTGFuZ1N0cmluZyBMaWNlbnNlVGV4dCBMb2FkQW5kU2V0SW1hZ2UgTG9hZExhbmd1YWdlRmlsZSBMb2NrV2luZG93IExvZ1NldCBMb2dUZXh0IE1hbmlmZXN0RFBJQXdhcmUgTWFuaWZlc3RMb25nUGF0aEF3YXJlIE1hbmlmZXN0TWF4VmVyc2lvblRlc3RlZCBNYW5pZmVzdFN1cHBvcnRlZE9TIE1lc3NhZ2VCb3ggTWlzY0J1dHRvblRleHQgTmFtZSBOb3AgT3V0RmlsZSBQYWdlIFBhZ2VDYWxsYmFja3MgUEVBZGRSZXNvdXJjZSBQRURsbENoYXJhY3RlcmlzdGljcyBQRVJlbW92ZVJlc291cmNlIFBFU3Vic3lzVmVyIFBvcCBQdXNoIFF1aXQgUmVhZEVudlN0ciBSZWFkSU5JU3RyIFJlYWRSZWdEV09SRCBSZWFkUmVnU3RyIFJlYm9vdCBSZWdETEwgUmVuYW1lIFJlcXVlc3RFeGVjdXRpb25MZXZlbCBSZXNlcnZlRmlsZSBSZXR1cm4gUk1EaXIgU2VhcmNoUGF0aCBTZWN0aW9uR2V0RmxhZ3MgU2VjdGlvbkdldEluc3RUeXBlcyBTZWN0aW9uR2V0U2l6ZSBTZWN0aW9uR2V0VGV4dCBTZWN0aW9uSW4gU2VjdGlvblNldEZsYWdzIFNlY3Rpb25TZXRJbnN0VHlwZXMgU2VjdGlvblNldFNpemUgU2VjdGlvblNldFRleHQgU2VuZE1lc3NhZ2UgU2V0QXV0b0Nsb3NlIFNldEJyYW5kaW5nSW1hZ2UgU2V0Q29tcHJlc3MgU2V0Q29tcHJlc3NvciBTZXRDb21wcmVzc29yRGljdFNpemUgU2V0Q3RsQ29sb3JzIFNldEN1ckluc3RUeXBlIFNldERhdGFibG9ja09wdGltaXplIFNldERhdGVTYXZlIFNldERldGFpbHNQcmludCBTZXREZXRhaWxzVmlldyBTZXRFcnJvckxldmVsIFNldEVycm9ycyBTZXRGaWxlQXR0cmlidXRlcyBTZXRGb250IFNldE91dFBhdGggU2V0T3ZlcndyaXRlIFNldFJlYm9vdEZsYWcgU2V0UmVnVmlldyBTZXRTaGVsbFZhckNvbnRleHQgU2V0U2lsZW50IFNob3dJbnN0RGV0YWlscyBTaG93VW5pbnN0RGV0YWlscyBTaG93V2luZG93IFNpbGVudEluc3RhbGwgU2lsZW50VW5JbnN0YWxsIFNsZWVwIFNwYWNlVGV4dHMgU3RyQ21wIFN0ckNtcFMgU3RyQ3B5IFN0ckxlbiBTdWJDYXB0aW9uIFVuaWNvZGUgVW5pbnN0YWxsQnV0dG9uVGV4dCBVbmluc3RhbGxDYXB0aW9uIFVuaW5zdGFsbEljb24gVW5pbnN0YWxsU3ViQ2FwdGlvbiBVbmluc3RhbGxUZXh0IFVuaW5zdFBhZ2UgVW5SZWdETEwgVmFyIFZJQWRkVmVyc2lvbktleSBWSUZpbGVWZXJzaW9uIFZJUHJvZHVjdFZlcnNpb24gV2luZG93SWNvbiBXcml0ZUlOSVN0ciBXcml0ZVJlZ0JpbiBXcml0ZVJlZ0RXT1JEIFdyaXRlUmVnRXhwYW5kU3RyIFdyaXRlUmVnTXVsdGlTdHIgV3JpdGVSZWdOb25lIFdyaXRlUmVnU3RyIFdyaXRlVW5pbnN0YWxsZXIgWFBTdHlsZScsXG4gICAgICBsaXRlcmFsOlxuICAgICAgJ2FkbWluIGFsbCBhdXRvIGJvdGggYm90dG9tIGJ6aXAyIGNvbG9yZWQgY29tcG9uZW50cyBjdXJyZW50IGN1c3RvbSBkaXJlY3RvcnkgZmFsc2UgZm9yY2UgaGlkZSBoaWdoZXN0IGlmZGlmZiBpZm5ld2VyIGluc3RmaWxlcyBsYXN0dXNlZCBsZWF2ZSBsZWZ0IGxpY2Vuc2UgbGlzdG9ubHkgbHptYSBuZXZlcnNob3cgbm9uZSBub3JtYWwgbm90c2V0IG9mZiBvbiBvcGVuIHByaW50IHJpZ2h0IHNob3cgc2lsZW50IHNpbGVudGxvZyBzbW9vdGggdGV4dG9ubHkgdG9wIHRydWUgdHJ5IHVuLmNvbXBvbmVudHMgdW4uY3VzdG9tIHVuLmRpcmVjdG9yeSB1bi5pbnN0ZmlsZXMgdW4ubGljZW5zZSB1bmluc3RDb25maXJtIHVzZXIgV2luMTAgV2luNyBXaW44IFdpblZpc3RhIHpsaWInXG4gICAgfSxcbiAgICBjb250YWluczogW1xuICAgICAgaGxqcy5IQVNIX0NPTU1FTlRfTU9ERSxcbiAgICAgIGhsanMuQ19CTE9DS19DT01NRU5UX01PREUsXG4gICAgICBobGpzLkNPTU1FTlQoXG4gICAgICAgICc7JyxcbiAgICAgICAgJyQnLFxuICAgICAgICB7XG4gICAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICAgIH1cbiAgICAgICksXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ2Z1bmN0aW9uJyxcbiAgICAgICAgYmVnaW5LZXl3b3JkczogJ0Z1bmN0aW9uIFBhZ2VFeCBTZWN0aW9uIFNlY3Rpb25Hcm91cCcsXG4gICAgICAgIGVuZDogJyQnXG4gICAgICB9LFxuICAgICAgU1RSSU5HLFxuICAgICAgQ09NUElMRVIsXG4gICAgICBERUZJTkVTLFxuICAgICAgVkFSSUFCTEVTLFxuICAgICAgTEFOR1VBR0VTLFxuICAgICAgUEFSQU1FVEVSUyxcbiAgICAgIFBMVUdJTlMsXG4gICAgICBobGpzLk5VTUJFUl9NT0RFXG4gICAgXVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IG5zaXM7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=