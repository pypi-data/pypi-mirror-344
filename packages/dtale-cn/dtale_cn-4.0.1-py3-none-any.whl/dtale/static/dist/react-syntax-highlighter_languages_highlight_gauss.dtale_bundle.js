(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_gauss"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/gauss.js":
/*!************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/gauss.js ***!
  \************************************************************************************************/
/***/ ((module) => {

/*
Language: GAUSS
Author: Matt Evans <matt@aptech.com>
Description: GAUSS Mathematical and Statistical language
Website: https://www.aptech.com
Category: scientific
*/
function gauss(hljs) {
  const KEYWORDS = {
    keyword: 'bool break call callexe checkinterrupt clear clearg closeall cls comlog compile ' +
              'continue create debug declare delete disable dlibrary dllcall do dos ed edit else ' +
              'elseif enable end endfor endif endp endo errorlog errorlogat expr external fn ' +
              'for format goto gosub graph if keyword let lib library line load loadarray loadexe ' +
              'loadf loadk loadm loadp loads loadx local locate loopnextindex lprint lpwidth lshow ' +
              'matrix msym ndpclex new open output outwidth plot plotsym pop prcsn print ' +
              'printdos proc push retp return rndcon rndmod rndmult rndseed run save saveall screen ' +
              'scroll setarray show sparse stop string struct system trace trap threadfor ' +
              'threadendfor threadbegin threadjoin threadstat threadend until use while winprint ' +
              'ne ge le gt lt and xor or not eq eqv',
    built_in: 'abs acf aconcat aeye amax amean AmericanBinomCall AmericanBinomCall_Greeks AmericanBinomCall_ImpVol ' +
              'AmericanBinomPut AmericanBinomPut_Greeks AmericanBinomPut_ImpVol AmericanBSCall AmericanBSCall_Greeks ' +
              'AmericanBSCall_ImpVol AmericanBSPut AmericanBSPut_Greeks AmericanBSPut_ImpVol amin amult annotationGetDefaults ' +
              'annotationSetBkd annotationSetFont annotationSetLineColor annotationSetLineStyle annotationSetLineThickness ' +
              'annualTradingDays arccos arcsin areshape arrayalloc arrayindex arrayinit arraytomat asciiload asclabel astd ' +
              'astds asum atan atan2 atranspose axmargin balance band bandchol bandcholsol bandltsol bandrv bandsolpd bar ' +
              'base10 begwind besselj bessely beta box boxcox cdfBeta cdfBetaInv cdfBinomial cdfBinomialInv cdfBvn cdfBvn2 ' +
              'cdfBvn2e cdfCauchy cdfCauchyInv cdfChic cdfChii cdfChinc cdfChincInv cdfExp cdfExpInv cdfFc cdfFnc cdfFncInv ' +
              'cdfGam cdfGenPareto cdfHyperGeo cdfLaplace cdfLaplaceInv cdfLogistic cdfLogisticInv cdfmControlCreate cdfMvn ' +
              'cdfMvn2e cdfMvnce cdfMvne cdfMvt2e cdfMvtce cdfMvte cdfN cdfN2 cdfNc cdfNegBinomial cdfNegBinomialInv cdfNi ' +
              'cdfPoisson cdfPoissonInv cdfRayleigh cdfRayleighInv cdfTc cdfTci cdfTnc cdfTvn cdfWeibull cdfWeibullInv cdir ' +
              'ceil ChangeDir chdir chiBarSquare chol choldn cholsol cholup chrs close code cols colsf combinate combinated ' +
              'complex con cond conj cons ConScore contour conv convertsatostr convertstrtosa corrm corrms corrvc corrx corrxs ' +
              'cos cosh counts countwts crossprd crout croutp csrcol csrlin csvReadM csvReadSA cumprodc cumsumc curve cvtos ' +
              'datacreate datacreatecomplex datalist dataload dataloop dataopen datasave date datestr datestring datestrymd ' +
              'dayinyr dayofweek dbAddDatabase dbClose dbCommit dbCreateQuery dbExecQuery dbGetConnectOptions dbGetDatabaseName ' +
              'dbGetDriverName dbGetDrivers dbGetHostName dbGetLastErrorNum dbGetLastErrorText dbGetNumericalPrecPolicy ' +
              'dbGetPassword dbGetPort dbGetTableHeaders dbGetTables dbGetUserName dbHasFeature dbIsDriverAvailable dbIsOpen ' +
              'dbIsOpenError dbOpen dbQueryBindValue dbQueryClear dbQueryCols dbQueryExecPrepared dbQueryFetchAllM dbQueryFetchAllSA ' +
              'dbQueryFetchOneM dbQueryFetchOneSA dbQueryFinish dbQueryGetBoundValue dbQueryGetBoundValues dbQueryGetField ' +
              'dbQueryGetLastErrorNum dbQueryGetLastErrorText dbQueryGetLastInsertID dbQueryGetLastQuery dbQueryGetPosition ' +
              'dbQueryIsActive dbQueryIsForwardOnly dbQueryIsNull dbQueryIsSelect dbQueryIsValid dbQueryPrepare dbQueryRows ' +
              'dbQuerySeek dbQuerySeekFirst dbQuerySeekLast dbQuerySeekNext dbQuerySeekPrevious dbQuerySetForwardOnly ' +
              'dbRemoveDatabase dbRollback dbSetConnectOptions dbSetDatabaseName dbSetHostName dbSetNumericalPrecPolicy ' +
              'dbSetPort dbSetUserName dbTransaction DeleteFile delif delrows denseToSp denseToSpRE denToZero design det detl ' +
              'dfft dffti diag diagrv digamma doswin DOSWinCloseall DOSWinOpen dotfeq dotfeqmt dotfge dotfgemt dotfgt dotfgtmt ' +
              'dotfle dotflemt dotflt dotfltmt dotfne dotfnemt draw drop dsCreate dstat dstatmt dstatmtControlCreate dtdate dtday ' +
              'dttime dttodtv dttostr dttoutc dtvnormal dtvtodt dtvtoutc dummy dummybr dummydn eig eigh eighv eigv elapsedTradingDays ' +
              'endwind envget eof eqSolve eqSolvemt eqSolvemtControlCreate eqSolvemtOutCreate eqSolveset erf erfc erfccplx erfcplx error ' +
              'etdays ethsec etstr EuropeanBinomCall EuropeanBinomCall_Greeks EuropeanBinomCall_ImpVol EuropeanBinomPut ' +
              'EuropeanBinomPut_Greeks EuropeanBinomPut_ImpVol EuropeanBSCall EuropeanBSCall_Greeks EuropeanBSCall_ImpVol ' +
              'EuropeanBSPut EuropeanBSPut_Greeks EuropeanBSPut_ImpVol exctsmpl exec execbg exp extern eye fcheckerr fclearerr feq ' +
              'feqmt fflush fft ffti fftm fftmi fftn fge fgemt fgets fgetsa fgetsat fgetst fgt fgtmt fileinfo filesa fle flemt ' +
              'floor flt fltmt fmod fne fnemt fonts fopen formatcv formatnv fputs fputst fseek fstrerror ftell ftocv ftos ftostrC ' +
              'gamma gammacplx gammaii gausset gdaAppend gdaCreate gdaDStat gdaDStatMat gdaGetIndex gdaGetName gdaGetNames gdaGetOrders ' +
              'gdaGetType gdaGetTypes gdaGetVarInfo gdaIsCplx gdaLoad gdaPack gdaRead gdaReadByIndex gdaReadSome gdaReadSparse ' +
              'gdaReadStruct gdaReportVarInfo gdaSave gdaUpdate gdaUpdateAndPack gdaVars gdaWrite gdaWrite32 gdaWriteSome getarray ' +
              'getdims getf getGAUSShome getmatrix getmatrix4D getname getnamef getNextTradingDay getNextWeekDay getnr getorders ' +
              'getpath getPreviousTradingDay getPreviousWeekDay getRow getscalar3D getscalar4D getTrRow getwind glm gradcplx gradMT ' +
              'gradMTm gradMTT gradMTTm gradp graphprt graphset hasimag header headermt hess hessMT hessMTg hessMTgw hessMTm ' +
              'hessMTmw hessMTT hessMTTg hessMTTgw hessMTTm hessMTw hessp hist histf histp hsec imag indcv indexcat indices indices2 ' +
              'indicesf indicesfn indnv indsav integrate1d integrateControlCreate intgrat2 intgrat3 inthp1 inthp2 inthp3 inthp4 ' +
              'inthpControlCreate intquad1 intquad2 intquad3 intrleav intrleavsa intrsect intsimp inv invpd invswp iscplx iscplxf ' +
              'isden isinfnanmiss ismiss key keyav keyw lag lag1 lagn lapEighb lapEighi lapEighvb lapEighvi lapgEig lapgEigh lapgEighv ' +
              'lapgEigv lapgSchur lapgSvdcst lapgSvds lapgSvdst lapSvdcusv lapSvds lapSvdusv ldlp ldlsol linSolve listwise ln lncdfbvn ' +
              'lncdfbvn2 lncdfmvn lncdfn lncdfn2 lncdfnc lnfact lngammacplx lnpdfmvn lnpdfmvt lnpdfn lnpdft loadd loadstruct loadwind ' +
              'loess loessmt loessmtControlCreate log loglog logx logy lower lowmat lowmat1 ltrisol lu lusol machEpsilon make makevars ' +
              'makewind margin matalloc matinit mattoarray maxbytes maxc maxindc maxv maxvec mbesselei mbesselei0 mbesselei1 mbesseli ' +
              'mbesseli0 mbesseli1 meanc median mergeby mergevar minc minindc minv miss missex missrv moment momentd movingave ' +
              'movingaveExpwgt movingaveWgt nextindex nextn nextnevn nextwind ntos null null1 numCombinations ols olsmt olsmtControlCreate ' +
              'olsqr olsqr2 olsqrmt ones optn optnevn orth outtyp pacf packedToSp packr parse pause pdfCauchy pdfChi pdfExp pdfGenPareto ' +
              'pdfHyperGeo pdfLaplace pdfLogistic pdfn pdfPoisson pdfRayleigh pdfWeibull pi pinv pinvmt plotAddArrow plotAddBar plotAddBox ' +
              'plotAddHist plotAddHistF plotAddHistP plotAddPolar plotAddScatter plotAddShape plotAddTextbox plotAddTS plotAddXY plotArea ' +
              'plotBar plotBox plotClearLayout plotContour plotCustomLayout plotGetDefaults plotHist plotHistF plotHistP plotLayout ' +
              'plotLogLog plotLogX plotLogY plotOpenWindow plotPolar plotSave plotScatter plotSetAxesPen plotSetBar plotSetBarFill ' +
              'plotSetBarStacked plotSetBkdColor plotSetFill plotSetGrid plotSetLegend plotSetLineColor plotSetLineStyle plotSetLineSymbol ' +
              'plotSetLineThickness plotSetNewWindow plotSetTitle plotSetWhichYAxis plotSetXAxisShow plotSetXLabel plotSetXRange ' +
              'plotSetXTicInterval plotSetXTicLabel plotSetYAxisShow plotSetYLabel plotSetYRange plotSetZAxisShow plotSetZLabel ' +
              'plotSurface plotTS plotXY polar polychar polyeval polygamma polyint polymake polymat polymroot polymult polyroot ' +
              'pqgwin previousindex princomp printfm printfmt prodc psi putarray putf putvals pvCreate pvGetIndex pvGetParNames ' +
              'pvGetParVector pvLength pvList pvPack pvPacki pvPackm pvPackmi pvPacks pvPacksi pvPacksm pvPacksmi pvPutParVector ' +
              'pvTest pvUnpack QNewton QNewtonmt QNewtonmtControlCreate QNewtonmtOutCreate QNewtonSet QProg QProgmt QProgmtInCreate ' +
              'qqr qqre qqrep qr qre qrep qrsol qrtsol qtyr qtyre qtyrep quantile quantiled qyr qyre qyrep qz rank rankindx readr ' +
              'real reclassify reclassifyCuts recode recserar recsercp recserrc rerun rescale reshape rets rev rfft rffti rfftip rfftn ' +
              'rfftnp rfftp rndBernoulli rndBeta rndBinomial rndCauchy rndChiSquare rndCon rndCreateState rndExp rndGamma rndGeo rndGumbel ' +
              'rndHyperGeo rndi rndKMbeta rndKMgam rndKMi rndKMn rndKMnb rndKMp rndKMu rndKMvm rndLaplace rndLCbeta rndLCgam rndLCi rndLCn ' +
              'rndLCnb rndLCp rndLCu rndLCvm rndLogNorm rndMTu rndMVn rndMVt rndn rndnb rndNegBinomial rndp rndPoisson rndRayleigh ' +
              'rndStateSkip rndu rndvm rndWeibull rndWishart rotater round rows rowsf rref sampleData satostrC saved saveStruct savewind ' +
              'scale scale3d scalerr scalinfnanmiss scalmiss schtoc schur searchsourcepath seekr select selif seqa seqm setdif setdifsa ' +
              'setvars setvwrmode setwind shell shiftr sin singleindex sinh sleep solpd sortc sortcc sortd sorthc sorthcc sortind ' +
              'sortindc sortmc sortr sortrc spBiconjGradSol spChol spConjGradSol spCreate spDenseSubmat spDiagRvMat spEigv spEye spLDL ' +
              'spline spLU spNumNZE spOnes spreadSheetReadM spreadSheetReadSA spreadSheetWrite spScale spSubmat spToDense spTrTDense ' +
              'spTScalar spZeros sqpSolve sqpSolveMT sqpSolveMTControlCreate sqpSolveMTlagrangeCreate sqpSolveMToutCreate sqpSolveSet ' +
              'sqrt statements stdc stdsc stocv stof strcombine strindx strlen strput strrindx strsect strsplit strsplitPad strtodt ' +
              'strtof strtofcplx strtriml strtrimr strtrunc strtruncl strtruncpad strtruncr submat subscat substute subvec sumc sumr ' +
              'surface svd svd1 svd2 svdcusv svds svdusv sysstate tab tan tanh tempname ' +
              'time timedt timestr timeutc title tkf2eps tkf2ps tocart todaydt toeplitz token topolar trapchk ' +
              'trigamma trimr trunc type typecv typef union unionsa uniqindx uniqindxsa unique uniquesa upmat upmat1 upper utctodt ' +
              'utctodtv utrisol vals varCovMS varCovXS varget vargetl varmall varmares varput varputl vartypef vcm vcms vcx vcxs ' +
              'vec vech vecr vector vget view viewxyz vlist vnamecv volume vput vread vtypecv wait waitc walkindex where window ' +
              'writer xlabel xlsGetSheetCount xlsGetSheetSize xlsGetSheetTypes xlsMakeRange xlsReadM xlsReadSA xlsWrite xlsWriteM ' +
              'xlsWriteSA xpnd xtics xy xyz ylabel ytics zeros zeta zlabel ztics cdfEmpirical dot h5create h5open h5read h5readAttribute ' +
              'h5write h5writeAttribute ldl plotAddErrorBar plotAddSurface plotCDFEmpirical plotSetColormap plotSetContourLabels ' +
              'plotSetLegendFont plotSetTextInterpreter plotSetXTicCount plotSetYTicCount plotSetZLevels powerm strjoin sylvester ' +
              'strtrim',
    literal: 'DB_AFTER_LAST_ROW DB_ALL_TABLES DB_BATCH_OPERATIONS DB_BEFORE_FIRST_ROW DB_BLOB DB_EVENT_NOTIFICATIONS ' +
             'DB_FINISH_QUERY DB_HIGH_PRECISION DB_LAST_INSERT_ID DB_LOW_PRECISION_DOUBLE DB_LOW_PRECISION_INT32 ' +
             'DB_LOW_PRECISION_INT64 DB_LOW_PRECISION_NUMBERS DB_MULTIPLE_RESULT_SETS DB_NAMED_PLACEHOLDERS ' +
             'DB_POSITIONAL_PLACEHOLDERS DB_PREPARED_QUERIES DB_QUERY_SIZE DB_SIMPLE_LOCKING DB_SYSTEM_TABLES DB_TABLES ' +
             'DB_TRANSACTIONS DB_UNICODE DB_VIEWS __STDIN __STDOUT __STDERR __FILE_DIR'
  };

  const AT_COMMENT_MODE = hljs.COMMENT('@', '@');

  const PREPROCESSOR =
  {
    className: 'meta',
    begin: '#',
    end: '$',
    keywords: {
      'meta-keyword': 'define definecs|10 undef ifdef ifndef iflight ifdllcall ifmac ifos2win ifunix else endif lineson linesoff srcfile srcline'
    },
    contains: [
      {
        begin: /\\\n/,
        relevance: 0
      },
      {
        beginKeywords: 'include',
        end: '$',
        keywords: {
          'meta-keyword': 'include'
        },
        contains: [
          {
            className: 'meta-string',
            begin: '"',
            end: '"',
            illegal: '\\n'
          }
        ]
      },
      hljs.C_LINE_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE,
      AT_COMMENT_MODE
    ]
  };

  const STRUCT_TYPE =
  {
    begin: /\bstruct\s+/,
    end: /\s/,
    keywords: "struct",
    contains: [
      {
        className: "type",
        begin: hljs.UNDERSCORE_IDENT_RE,
        relevance: 0
      }
    ]
  };

  // only for definitions
  const PARSE_PARAMS = [
    {
      className: 'params',
      begin: /\(/,
      end: /\)/,
      excludeBegin: true,
      excludeEnd: true,
      endsWithParent: true,
      relevance: 0,
      contains: [
        { // dots
          className: 'literal',
          begin: /\.\.\./
        },
        hljs.C_NUMBER_MODE,
        hljs.C_BLOCK_COMMENT_MODE,
        AT_COMMENT_MODE,
        STRUCT_TYPE
      ]
    }
  ];

  const FUNCTION_DEF =
  {
    className: "title",
    begin: hljs.UNDERSCORE_IDENT_RE,
    relevance: 0
  };

  const DEFINITION = function(beginKeywords, end, inherits) {
    const mode = hljs.inherit(
      {
        className: "function",
        beginKeywords: beginKeywords,
        end: end,
        excludeEnd: true,
        contains: [].concat(PARSE_PARAMS)
      },
      inherits || {}
    );
    mode.contains.push(FUNCTION_DEF);
    mode.contains.push(hljs.C_NUMBER_MODE);
    mode.contains.push(hljs.C_BLOCK_COMMENT_MODE);
    mode.contains.push(AT_COMMENT_MODE);
    return mode;
  };

  const BUILT_IN_REF =
  { // these are explicitly named internal function calls
    className: 'built_in',
    begin: '\\b(' + KEYWORDS.built_in.split(' ').join('|') + ')\\b'
  };

  const STRING_REF =
  {
    className: 'string',
    begin: '"',
    end: '"',
    contains: [hljs.BACKSLASH_ESCAPE],
    relevance: 0
  };

  const FUNCTION_REF =
  {
    // className: "fn_ref",
    begin: hljs.UNDERSCORE_IDENT_RE + '\\s*\\(',
    returnBegin: true,
    keywords: KEYWORDS,
    relevance: 0,
    contains: [
      {
        beginKeywords: KEYWORDS.keyword
      },
      BUILT_IN_REF,
      { // ambiguously named function calls get a relevance of 0
        className: 'built_in',
        begin: hljs.UNDERSCORE_IDENT_RE,
        relevance: 0
      }
    ]
  };

  const FUNCTION_REF_PARAMS =
  {
    // className: "fn_ref_params",
    begin: /\(/,
    end: /\)/,
    relevance: 0,
    keywords: {
      built_in: KEYWORDS.built_in,
      literal: KEYWORDS.literal
    },
    contains: [
      hljs.C_NUMBER_MODE,
      hljs.C_BLOCK_COMMENT_MODE,
      AT_COMMENT_MODE,
      BUILT_IN_REF,
      FUNCTION_REF,
      STRING_REF,
      'self'
    ]
  };

  FUNCTION_REF.contains.push(FUNCTION_REF_PARAMS);

  return {
    name: 'GAUSS',
    aliases: ['gss'],
    case_insensitive: true, // language is case-insensitive
    keywords: KEYWORDS,
    illegal: /(\{[%#]|[%#]\}| <- )/,
    contains: [
      hljs.C_NUMBER_MODE,
      hljs.C_LINE_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE,
      AT_COMMENT_MODE,
      STRING_REF,
      PREPROCESSOR,
      {
        className: 'keyword',
        begin: /\bexternal (matrix|string|array|sparse matrix|struct|proc|keyword|fn)/
      },
      DEFINITION('proc keyword', ';'),
      DEFINITION('fn', '='),
      {
        beginKeywords: 'for threadfor',
        end: /;/,
        // end: /\(/,
        relevance: 0,
        contains: [
          hljs.C_BLOCK_COMMENT_MODE,
          AT_COMMENT_MODE,
          FUNCTION_REF_PARAMS
        ]
      },
      { // custom method guard
        // excludes method names from keyword processing
        variants: [
          {
            begin: hljs.UNDERSCORE_IDENT_RE + '\\.' + hljs.UNDERSCORE_IDENT_RE
          },
          {
            begin: hljs.UNDERSCORE_IDENT_RE + '\\s*='
          }
        ],
        relevance: 0
      },
      FUNCTION_REF,
      STRUCT_TYPE
    ]
  };
}

module.exports = gauss;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfZ2F1c3MuZHRhbGVfYnVuZGxlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsU0FBUztBQUNUO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsVUFBVTtBQUNWO0FBQ0E7QUFDQSxTQUFTO0FBQ1Q7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBLElBQUk7QUFDSjtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBLFFBQVE7QUFDUjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxpQkFBaUIsV0FBVztBQUM1QjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUCxtQ0FBbUM7QUFDbkM7QUFDQTtBQUNBO0FBQ0EsZUFBZTtBQUNmO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQLFFBQVE7QUFDUjtBQUNBO0FBQ0E7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL2dhdXNzLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogR0FVU1NcbkF1dGhvcjogTWF0dCBFdmFucyA8bWF0dEBhcHRlY2guY29tPlxuRGVzY3JpcHRpb246IEdBVVNTIE1hdGhlbWF0aWNhbCBhbmQgU3RhdGlzdGljYWwgbGFuZ3VhZ2VcbldlYnNpdGU6IGh0dHBzOi8vd3d3LmFwdGVjaC5jb21cbkNhdGVnb3J5OiBzY2llbnRpZmljXG4qL1xuZnVuY3Rpb24gZ2F1c3MoaGxqcykge1xuICBjb25zdCBLRVlXT1JEUyA9IHtcbiAgICBrZXl3b3JkOiAnYm9vbCBicmVhayBjYWxsIGNhbGxleGUgY2hlY2tpbnRlcnJ1cHQgY2xlYXIgY2xlYXJnIGNsb3NlYWxsIGNscyBjb21sb2cgY29tcGlsZSAnICtcbiAgICAgICAgICAgICAgJ2NvbnRpbnVlIGNyZWF0ZSBkZWJ1ZyBkZWNsYXJlIGRlbGV0ZSBkaXNhYmxlIGRsaWJyYXJ5IGRsbGNhbGwgZG8gZG9zIGVkIGVkaXQgZWxzZSAnICtcbiAgICAgICAgICAgICAgJ2Vsc2VpZiBlbmFibGUgZW5kIGVuZGZvciBlbmRpZiBlbmRwIGVuZG8gZXJyb3Jsb2cgZXJyb3Jsb2dhdCBleHByIGV4dGVybmFsIGZuICcgK1xuICAgICAgICAgICAgICAnZm9yIGZvcm1hdCBnb3RvIGdvc3ViIGdyYXBoIGlmIGtleXdvcmQgbGV0IGxpYiBsaWJyYXJ5IGxpbmUgbG9hZCBsb2FkYXJyYXkgbG9hZGV4ZSAnICtcbiAgICAgICAgICAgICAgJ2xvYWRmIGxvYWRrIGxvYWRtIGxvYWRwIGxvYWRzIGxvYWR4IGxvY2FsIGxvY2F0ZSBsb29wbmV4dGluZGV4IGxwcmludCBscHdpZHRoIGxzaG93ICcgK1xuICAgICAgICAgICAgICAnbWF0cml4IG1zeW0gbmRwY2xleCBuZXcgb3BlbiBvdXRwdXQgb3V0d2lkdGggcGxvdCBwbG90c3ltIHBvcCBwcmNzbiBwcmludCAnICtcbiAgICAgICAgICAgICAgJ3ByaW50ZG9zIHByb2MgcHVzaCByZXRwIHJldHVybiBybmRjb24gcm5kbW9kIHJuZG11bHQgcm5kc2VlZCBydW4gc2F2ZSBzYXZlYWxsIHNjcmVlbiAnICtcbiAgICAgICAgICAgICAgJ3Njcm9sbCBzZXRhcnJheSBzaG93IHNwYXJzZSBzdG9wIHN0cmluZyBzdHJ1Y3Qgc3lzdGVtIHRyYWNlIHRyYXAgdGhyZWFkZm9yICcgK1xuICAgICAgICAgICAgICAndGhyZWFkZW5kZm9yIHRocmVhZGJlZ2luIHRocmVhZGpvaW4gdGhyZWFkc3RhdCB0aHJlYWRlbmQgdW50aWwgdXNlIHdoaWxlIHdpbnByaW50ICcgK1xuICAgICAgICAgICAgICAnbmUgZ2UgbGUgZ3QgbHQgYW5kIHhvciBvciBub3QgZXEgZXF2JyxcbiAgICBidWlsdF9pbjogJ2FicyBhY2YgYWNvbmNhdCBhZXllIGFtYXggYW1lYW4gQW1lcmljYW5CaW5vbUNhbGwgQW1lcmljYW5CaW5vbUNhbGxfR3JlZWtzIEFtZXJpY2FuQmlub21DYWxsX0ltcFZvbCAnICtcbiAgICAgICAgICAgICAgJ0FtZXJpY2FuQmlub21QdXQgQW1lcmljYW5CaW5vbVB1dF9HcmVla3MgQW1lcmljYW5CaW5vbVB1dF9JbXBWb2wgQW1lcmljYW5CU0NhbGwgQW1lcmljYW5CU0NhbGxfR3JlZWtzICcgK1xuICAgICAgICAgICAgICAnQW1lcmljYW5CU0NhbGxfSW1wVm9sIEFtZXJpY2FuQlNQdXQgQW1lcmljYW5CU1B1dF9HcmVla3MgQW1lcmljYW5CU1B1dF9JbXBWb2wgYW1pbiBhbXVsdCBhbm5vdGF0aW9uR2V0RGVmYXVsdHMgJyArXG4gICAgICAgICAgICAgICdhbm5vdGF0aW9uU2V0QmtkIGFubm90YXRpb25TZXRGb250IGFubm90YXRpb25TZXRMaW5lQ29sb3IgYW5ub3RhdGlvblNldExpbmVTdHlsZSBhbm5vdGF0aW9uU2V0TGluZVRoaWNrbmVzcyAnICtcbiAgICAgICAgICAgICAgJ2FubnVhbFRyYWRpbmdEYXlzIGFyY2NvcyBhcmNzaW4gYXJlc2hhcGUgYXJyYXlhbGxvYyBhcnJheWluZGV4IGFycmF5aW5pdCBhcnJheXRvbWF0IGFzY2lpbG9hZCBhc2NsYWJlbCBhc3RkICcgK1xuICAgICAgICAgICAgICAnYXN0ZHMgYXN1bSBhdGFuIGF0YW4yIGF0cmFuc3Bvc2UgYXhtYXJnaW4gYmFsYW5jZSBiYW5kIGJhbmRjaG9sIGJhbmRjaG9sc29sIGJhbmRsdHNvbCBiYW5kcnYgYmFuZHNvbHBkIGJhciAnICtcbiAgICAgICAgICAgICAgJ2Jhc2UxMCBiZWd3aW5kIGJlc3NlbGogYmVzc2VseSBiZXRhIGJveCBib3hjb3ggY2RmQmV0YSBjZGZCZXRhSW52IGNkZkJpbm9taWFsIGNkZkJpbm9taWFsSW52IGNkZkJ2biBjZGZCdm4yICcgK1xuICAgICAgICAgICAgICAnY2RmQnZuMmUgY2RmQ2F1Y2h5IGNkZkNhdWNoeUludiBjZGZDaGljIGNkZkNoaWkgY2RmQ2hpbmMgY2RmQ2hpbmNJbnYgY2RmRXhwIGNkZkV4cEludiBjZGZGYyBjZGZGbmMgY2RmRm5jSW52ICcgK1xuICAgICAgICAgICAgICAnY2RmR2FtIGNkZkdlblBhcmV0byBjZGZIeXBlckdlbyBjZGZMYXBsYWNlIGNkZkxhcGxhY2VJbnYgY2RmTG9naXN0aWMgY2RmTG9naXN0aWNJbnYgY2RmbUNvbnRyb2xDcmVhdGUgY2RmTXZuICcgK1xuICAgICAgICAgICAgICAnY2RmTXZuMmUgY2RmTXZuY2UgY2RmTXZuZSBjZGZNdnQyZSBjZGZNdnRjZSBjZGZNdnRlIGNkZk4gY2RmTjIgY2RmTmMgY2RmTmVnQmlub21pYWwgY2RmTmVnQmlub21pYWxJbnYgY2RmTmkgJyArXG4gICAgICAgICAgICAgICdjZGZQb2lzc29uIGNkZlBvaXNzb25JbnYgY2RmUmF5bGVpZ2ggY2RmUmF5bGVpZ2hJbnYgY2RmVGMgY2RmVGNpIGNkZlRuYyBjZGZUdm4gY2RmV2VpYnVsbCBjZGZXZWlidWxsSW52IGNkaXIgJyArXG4gICAgICAgICAgICAgICdjZWlsIENoYW5nZURpciBjaGRpciBjaGlCYXJTcXVhcmUgY2hvbCBjaG9sZG4gY2hvbHNvbCBjaG9sdXAgY2hycyBjbG9zZSBjb2RlIGNvbHMgY29sc2YgY29tYmluYXRlIGNvbWJpbmF0ZWQgJyArXG4gICAgICAgICAgICAgICdjb21wbGV4IGNvbiBjb25kIGNvbmogY29ucyBDb25TY29yZSBjb250b3VyIGNvbnYgY29udmVydHNhdG9zdHIgY29udmVydHN0cnRvc2EgY29ycm0gY29ycm1zIGNvcnJ2YyBjb3JyeCBjb3JyeHMgJyArXG4gICAgICAgICAgICAgICdjb3MgY29zaCBjb3VudHMgY291bnR3dHMgY3Jvc3NwcmQgY3JvdXQgY3JvdXRwIGNzcmNvbCBjc3JsaW4gY3N2UmVhZE0gY3N2UmVhZFNBIGN1bXByb2RjIGN1bXN1bWMgY3VydmUgY3Z0b3MgJyArXG4gICAgICAgICAgICAgICdkYXRhY3JlYXRlIGRhdGFjcmVhdGVjb21wbGV4IGRhdGFsaXN0IGRhdGFsb2FkIGRhdGFsb29wIGRhdGFvcGVuIGRhdGFzYXZlIGRhdGUgZGF0ZXN0ciBkYXRlc3RyaW5nIGRhdGVzdHJ5bWQgJyArXG4gICAgICAgICAgICAgICdkYXlpbnlyIGRheW9md2VlayBkYkFkZERhdGFiYXNlIGRiQ2xvc2UgZGJDb21taXQgZGJDcmVhdGVRdWVyeSBkYkV4ZWNRdWVyeSBkYkdldENvbm5lY3RPcHRpb25zIGRiR2V0RGF0YWJhc2VOYW1lICcgK1xuICAgICAgICAgICAgICAnZGJHZXREcml2ZXJOYW1lIGRiR2V0RHJpdmVycyBkYkdldEhvc3ROYW1lIGRiR2V0TGFzdEVycm9yTnVtIGRiR2V0TGFzdEVycm9yVGV4dCBkYkdldE51bWVyaWNhbFByZWNQb2xpY3kgJyArXG4gICAgICAgICAgICAgICdkYkdldFBhc3N3b3JkIGRiR2V0UG9ydCBkYkdldFRhYmxlSGVhZGVycyBkYkdldFRhYmxlcyBkYkdldFVzZXJOYW1lIGRiSGFzRmVhdHVyZSBkYklzRHJpdmVyQXZhaWxhYmxlIGRiSXNPcGVuICcgK1xuICAgICAgICAgICAgICAnZGJJc09wZW5FcnJvciBkYk9wZW4gZGJRdWVyeUJpbmRWYWx1ZSBkYlF1ZXJ5Q2xlYXIgZGJRdWVyeUNvbHMgZGJRdWVyeUV4ZWNQcmVwYXJlZCBkYlF1ZXJ5RmV0Y2hBbGxNIGRiUXVlcnlGZXRjaEFsbFNBICcgK1xuICAgICAgICAgICAgICAnZGJRdWVyeUZldGNoT25lTSBkYlF1ZXJ5RmV0Y2hPbmVTQSBkYlF1ZXJ5RmluaXNoIGRiUXVlcnlHZXRCb3VuZFZhbHVlIGRiUXVlcnlHZXRCb3VuZFZhbHVlcyBkYlF1ZXJ5R2V0RmllbGQgJyArXG4gICAgICAgICAgICAgICdkYlF1ZXJ5R2V0TGFzdEVycm9yTnVtIGRiUXVlcnlHZXRMYXN0RXJyb3JUZXh0IGRiUXVlcnlHZXRMYXN0SW5zZXJ0SUQgZGJRdWVyeUdldExhc3RRdWVyeSBkYlF1ZXJ5R2V0UG9zaXRpb24gJyArXG4gICAgICAgICAgICAgICdkYlF1ZXJ5SXNBY3RpdmUgZGJRdWVyeUlzRm9yd2FyZE9ubHkgZGJRdWVyeUlzTnVsbCBkYlF1ZXJ5SXNTZWxlY3QgZGJRdWVyeUlzVmFsaWQgZGJRdWVyeVByZXBhcmUgZGJRdWVyeVJvd3MgJyArXG4gICAgICAgICAgICAgICdkYlF1ZXJ5U2VlayBkYlF1ZXJ5U2Vla0ZpcnN0IGRiUXVlcnlTZWVrTGFzdCBkYlF1ZXJ5U2Vla05leHQgZGJRdWVyeVNlZWtQcmV2aW91cyBkYlF1ZXJ5U2V0Rm9yd2FyZE9ubHkgJyArXG4gICAgICAgICAgICAgICdkYlJlbW92ZURhdGFiYXNlIGRiUm9sbGJhY2sgZGJTZXRDb25uZWN0T3B0aW9ucyBkYlNldERhdGFiYXNlTmFtZSBkYlNldEhvc3ROYW1lIGRiU2V0TnVtZXJpY2FsUHJlY1BvbGljeSAnICtcbiAgICAgICAgICAgICAgJ2RiU2V0UG9ydCBkYlNldFVzZXJOYW1lIGRiVHJhbnNhY3Rpb24gRGVsZXRlRmlsZSBkZWxpZiBkZWxyb3dzIGRlbnNlVG9TcCBkZW5zZVRvU3BSRSBkZW5Ub1plcm8gZGVzaWduIGRldCBkZXRsICcgK1xuICAgICAgICAgICAgICAnZGZmdCBkZmZ0aSBkaWFnIGRpYWdydiBkaWdhbW1hIGRvc3dpbiBET1NXaW5DbG9zZWFsbCBET1NXaW5PcGVuIGRvdGZlcSBkb3RmZXFtdCBkb3RmZ2UgZG90ZmdlbXQgZG90Zmd0IGRvdGZndG10ICcgK1xuICAgICAgICAgICAgICAnZG90ZmxlIGRvdGZsZW10IGRvdGZsdCBkb3RmbHRtdCBkb3RmbmUgZG90Zm5lbXQgZHJhdyBkcm9wIGRzQ3JlYXRlIGRzdGF0IGRzdGF0bXQgZHN0YXRtdENvbnRyb2xDcmVhdGUgZHRkYXRlIGR0ZGF5ICcgK1xuICAgICAgICAgICAgICAnZHR0aW1lIGR0dG9kdHYgZHR0b3N0ciBkdHRvdXRjIGR0dm5vcm1hbCBkdHZ0b2R0IGR0dnRvdXRjIGR1bW15IGR1bW15YnIgZHVtbXlkbiBlaWcgZWlnaCBlaWdodiBlaWd2IGVsYXBzZWRUcmFkaW5nRGF5cyAnICtcbiAgICAgICAgICAgICAgJ2VuZHdpbmQgZW52Z2V0IGVvZiBlcVNvbHZlIGVxU29sdmVtdCBlcVNvbHZlbXRDb250cm9sQ3JlYXRlIGVxU29sdmVtdE91dENyZWF0ZSBlcVNvbHZlc2V0IGVyZiBlcmZjIGVyZmNjcGx4IGVyZmNwbHggZXJyb3IgJyArXG4gICAgICAgICAgICAgICdldGRheXMgZXRoc2VjIGV0c3RyIEV1cm9wZWFuQmlub21DYWxsIEV1cm9wZWFuQmlub21DYWxsX0dyZWVrcyBFdXJvcGVhbkJpbm9tQ2FsbF9JbXBWb2wgRXVyb3BlYW5CaW5vbVB1dCAnICtcbiAgICAgICAgICAgICAgJ0V1cm9wZWFuQmlub21QdXRfR3JlZWtzIEV1cm9wZWFuQmlub21QdXRfSW1wVm9sIEV1cm9wZWFuQlNDYWxsIEV1cm9wZWFuQlNDYWxsX0dyZWVrcyBFdXJvcGVhbkJTQ2FsbF9JbXBWb2wgJyArXG4gICAgICAgICAgICAgICdFdXJvcGVhbkJTUHV0IEV1cm9wZWFuQlNQdXRfR3JlZWtzIEV1cm9wZWFuQlNQdXRfSW1wVm9sIGV4Y3RzbXBsIGV4ZWMgZXhlY2JnIGV4cCBleHRlcm4gZXllIGZjaGVja2VyciBmY2xlYXJlcnIgZmVxICcgK1xuICAgICAgICAgICAgICAnZmVxbXQgZmZsdXNoIGZmdCBmZnRpIGZmdG0gZmZ0bWkgZmZ0biBmZ2UgZmdlbXQgZmdldHMgZmdldHNhIGZnZXRzYXQgZmdldHN0IGZndCBmZ3RtdCBmaWxlaW5mbyBmaWxlc2EgZmxlIGZsZW10ICcgK1xuICAgICAgICAgICAgICAnZmxvb3IgZmx0IGZsdG10IGZtb2QgZm5lIGZuZW10IGZvbnRzIGZvcGVuIGZvcm1hdGN2IGZvcm1hdG52IGZwdXRzIGZwdXRzdCBmc2VlayBmc3RyZXJyb3IgZnRlbGwgZnRvY3YgZnRvcyBmdG9zdHJDICcgK1xuICAgICAgICAgICAgICAnZ2FtbWEgZ2FtbWFjcGx4IGdhbW1haWkgZ2F1c3NldCBnZGFBcHBlbmQgZ2RhQ3JlYXRlIGdkYURTdGF0IGdkYURTdGF0TWF0IGdkYUdldEluZGV4IGdkYUdldE5hbWUgZ2RhR2V0TmFtZXMgZ2RhR2V0T3JkZXJzICcgK1xuICAgICAgICAgICAgICAnZ2RhR2V0VHlwZSBnZGFHZXRUeXBlcyBnZGFHZXRWYXJJbmZvIGdkYUlzQ3BseCBnZGFMb2FkIGdkYVBhY2sgZ2RhUmVhZCBnZGFSZWFkQnlJbmRleCBnZGFSZWFkU29tZSBnZGFSZWFkU3BhcnNlICcgK1xuICAgICAgICAgICAgICAnZ2RhUmVhZFN0cnVjdCBnZGFSZXBvcnRWYXJJbmZvIGdkYVNhdmUgZ2RhVXBkYXRlIGdkYVVwZGF0ZUFuZFBhY2sgZ2RhVmFycyBnZGFXcml0ZSBnZGFXcml0ZTMyIGdkYVdyaXRlU29tZSBnZXRhcnJheSAnICtcbiAgICAgICAgICAgICAgJ2dldGRpbXMgZ2V0ZiBnZXRHQVVTU2hvbWUgZ2V0bWF0cml4IGdldG1hdHJpeDREIGdldG5hbWUgZ2V0bmFtZWYgZ2V0TmV4dFRyYWRpbmdEYXkgZ2V0TmV4dFdlZWtEYXkgZ2V0bnIgZ2V0b3JkZXJzICcgK1xuICAgICAgICAgICAgICAnZ2V0cGF0aCBnZXRQcmV2aW91c1RyYWRpbmdEYXkgZ2V0UHJldmlvdXNXZWVrRGF5IGdldFJvdyBnZXRzY2FsYXIzRCBnZXRzY2FsYXI0RCBnZXRUclJvdyBnZXR3aW5kIGdsbSBncmFkY3BseCBncmFkTVQgJyArXG4gICAgICAgICAgICAgICdncmFkTVRtIGdyYWRNVFQgZ3JhZE1UVG0gZ3JhZHAgZ3JhcGhwcnQgZ3JhcGhzZXQgaGFzaW1hZyBoZWFkZXIgaGVhZGVybXQgaGVzcyBoZXNzTVQgaGVzc01UZyBoZXNzTVRndyBoZXNzTVRtICcgK1xuICAgICAgICAgICAgICAnaGVzc01UbXcgaGVzc01UVCBoZXNzTVRUZyBoZXNzTVRUZ3cgaGVzc01UVG0gaGVzc01UdyBoZXNzcCBoaXN0IGhpc3RmIGhpc3RwIGhzZWMgaW1hZyBpbmRjdiBpbmRleGNhdCBpbmRpY2VzIGluZGljZXMyICcgK1xuICAgICAgICAgICAgICAnaW5kaWNlc2YgaW5kaWNlc2ZuIGluZG52IGluZHNhdiBpbnRlZ3JhdGUxZCBpbnRlZ3JhdGVDb250cm9sQ3JlYXRlIGludGdyYXQyIGludGdyYXQzIGludGhwMSBpbnRocDIgaW50aHAzIGludGhwNCAnICtcbiAgICAgICAgICAgICAgJ2ludGhwQ29udHJvbENyZWF0ZSBpbnRxdWFkMSBpbnRxdWFkMiBpbnRxdWFkMyBpbnRybGVhdiBpbnRybGVhdnNhIGludHJzZWN0IGludHNpbXAgaW52IGludnBkIGludnN3cCBpc2NwbHggaXNjcGx4ZiAnICtcbiAgICAgICAgICAgICAgJ2lzZGVuIGlzaW5mbmFubWlzcyBpc21pc3Mga2V5IGtleWF2IGtleXcgbGFnIGxhZzEgbGFnbiBsYXBFaWdoYiBsYXBFaWdoaSBsYXBFaWdodmIgbGFwRWlnaHZpIGxhcGdFaWcgbGFwZ0VpZ2ggbGFwZ0VpZ2h2ICcgK1xuICAgICAgICAgICAgICAnbGFwZ0VpZ3YgbGFwZ1NjaHVyIGxhcGdTdmRjc3QgbGFwZ1N2ZHMgbGFwZ1N2ZHN0IGxhcFN2ZGN1c3YgbGFwU3ZkcyBsYXBTdmR1c3YgbGRscCBsZGxzb2wgbGluU29sdmUgbGlzdHdpc2UgbG4gbG5jZGZidm4gJyArXG4gICAgICAgICAgICAgICdsbmNkZmJ2bjIgbG5jZGZtdm4gbG5jZGZuIGxuY2RmbjIgbG5jZGZuYyBsbmZhY3QgbG5nYW1tYWNwbHggbG5wZGZtdm4gbG5wZGZtdnQgbG5wZGZuIGxucGRmdCBsb2FkZCBsb2Fkc3RydWN0IGxvYWR3aW5kICcgK1xuICAgICAgICAgICAgICAnbG9lc3MgbG9lc3NtdCBsb2Vzc210Q29udHJvbENyZWF0ZSBsb2cgbG9nbG9nIGxvZ3ggbG9neSBsb3dlciBsb3dtYXQgbG93bWF0MSBsdHJpc29sIGx1IGx1c29sIG1hY2hFcHNpbG9uIG1ha2UgbWFrZXZhcnMgJyArXG4gICAgICAgICAgICAgICdtYWtld2luZCBtYXJnaW4gbWF0YWxsb2MgbWF0aW5pdCBtYXR0b2FycmF5IG1heGJ5dGVzIG1heGMgbWF4aW5kYyBtYXh2IG1heHZlYyBtYmVzc2VsZWkgbWJlc3NlbGVpMCBtYmVzc2VsZWkxIG1iZXNzZWxpICcgK1xuICAgICAgICAgICAgICAnbWJlc3NlbGkwIG1iZXNzZWxpMSBtZWFuYyBtZWRpYW4gbWVyZ2VieSBtZXJnZXZhciBtaW5jIG1pbmluZGMgbWludiBtaXNzIG1pc3NleCBtaXNzcnYgbW9tZW50IG1vbWVudGQgbW92aW5nYXZlICcgK1xuICAgICAgICAgICAgICAnbW92aW5nYXZlRXhwd2d0IG1vdmluZ2F2ZVdndCBuZXh0aW5kZXggbmV4dG4gbmV4dG5ldm4gbmV4dHdpbmQgbnRvcyBudWxsIG51bGwxIG51bUNvbWJpbmF0aW9ucyBvbHMgb2xzbXQgb2xzbXRDb250cm9sQ3JlYXRlICcgK1xuICAgICAgICAgICAgICAnb2xzcXIgb2xzcXIyIG9sc3FybXQgb25lcyBvcHRuIG9wdG5ldm4gb3J0aCBvdXR0eXAgcGFjZiBwYWNrZWRUb1NwIHBhY2tyIHBhcnNlIHBhdXNlIHBkZkNhdWNoeSBwZGZDaGkgcGRmRXhwIHBkZkdlblBhcmV0byAnICtcbiAgICAgICAgICAgICAgJ3BkZkh5cGVyR2VvIHBkZkxhcGxhY2UgcGRmTG9naXN0aWMgcGRmbiBwZGZQb2lzc29uIHBkZlJheWxlaWdoIHBkZldlaWJ1bGwgcGkgcGludiBwaW52bXQgcGxvdEFkZEFycm93IHBsb3RBZGRCYXIgcGxvdEFkZEJveCAnICtcbiAgICAgICAgICAgICAgJ3Bsb3RBZGRIaXN0IHBsb3RBZGRIaXN0RiBwbG90QWRkSGlzdFAgcGxvdEFkZFBvbGFyIHBsb3RBZGRTY2F0dGVyIHBsb3RBZGRTaGFwZSBwbG90QWRkVGV4dGJveCBwbG90QWRkVFMgcGxvdEFkZFhZIHBsb3RBcmVhICcgK1xuICAgICAgICAgICAgICAncGxvdEJhciBwbG90Qm94IHBsb3RDbGVhckxheW91dCBwbG90Q29udG91ciBwbG90Q3VzdG9tTGF5b3V0IHBsb3RHZXREZWZhdWx0cyBwbG90SGlzdCBwbG90SGlzdEYgcGxvdEhpc3RQIHBsb3RMYXlvdXQgJyArXG4gICAgICAgICAgICAgICdwbG90TG9nTG9nIHBsb3RMb2dYIHBsb3RMb2dZIHBsb3RPcGVuV2luZG93IHBsb3RQb2xhciBwbG90U2F2ZSBwbG90U2NhdHRlciBwbG90U2V0QXhlc1BlbiBwbG90U2V0QmFyIHBsb3RTZXRCYXJGaWxsICcgK1xuICAgICAgICAgICAgICAncGxvdFNldEJhclN0YWNrZWQgcGxvdFNldEJrZENvbG9yIHBsb3RTZXRGaWxsIHBsb3RTZXRHcmlkIHBsb3RTZXRMZWdlbmQgcGxvdFNldExpbmVDb2xvciBwbG90U2V0TGluZVN0eWxlIHBsb3RTZXRMaW5lU3ltYm9sICcgK1xuICAgICAgICAgICAgICAncGxvdFNldExpbmVUaGlja25lc3MgcGxvdFNldE5ld1dpbmRvdyBwbG90U2V0VGl0bGUgcGxvdFNldFdoaWNoWUF4aXMgcGxvdFNldFhBeGlzU2hvdyBwbG90U2V0WExhYmVsIHBsb3RTZXRYUmFuZ2UgJyArXG4gICAgICAgICAgICAgICdwbG90U2V0WFRpY0ludGVydmFsIHBsb3RTZXRYVGljTGFiZWwgcGxvdFNldFlBeGlzU2hvdyBwbG90U2V0WUxhYmVsIHBsb3RTZXRZUmFuZ2UgcGxvdFNldFpBeGlzU2hvdyBwbG90U2V0WkxhYmVsICcgK1xuICAgICAgICAgICAgICAncGxvdFN1cmZhY2UgcGxvdFRTIHBsb3RYWSBwb2xhciBwb2x5Y2hhciBwb2x5ZXZhbCBwb2x5Z2FtbWEgcG9seWludCBwb2x5bWFrZSBwb2x5bWF0IHBvbHltcm9vdCBwb2x5bXVsdCBwb2x5cm9vdCAnICtcbiAgICAgICAgICAgICAgJ3BxZ3dpbiBwcmV2aW91c2luZGV4IHByaW5jb21wIHByaW50Zm0gcHJpbnRmbXQgcHJvZGMgcHNpIHB1dGFycmF5IHB1dGYgcHV0dmFscyBwdkNyZWF0ZSBwdkdldEluZGV4IHB2R2V0UGFyTmFtZXMgJyArXG4gICAgICAgICAgICAgICdwdkdldFBhclZlY3RvciBwdkxlbmd0aCBwdkxpc3QgcHZQYWNrIHB2UGFja2kgcHZQYWNrbSBwdlBhY2ttaSBwdlBhY2tzIHB2UGFja3NpIHB2UGFja3NtIHB2UGFja3NtaSBwdlB1dFBhclZlY3RvciAnICtcbiAgICAgICAgICAgICAgJ3B2VGVzdCBwdlVucGFjayBRTmV3dG9uIFFOZXd0b25tdCBRTmV3dG9ubXRDb250cm9sQ3JlYXRlIFFOZXd0b25tdE91dENyZWF0ZSBRTmV3dG9uU2V0IFFQcm9nIFFQcm9nbXQgUVByb2dtdEluQ3JlYXRlICcgK1xuICAgICAgICAgICAgICAncXFyIHFxcmUgcXFyZXAgcXIgcXJlIHFyZXAgcXJzb2wgcXJ0c29sIHF0eXIgcXR5cmUgcXR5cmVwIHF1YW50aWxlIHF1YW50aWxlZCBxeXIgcXlyZSBxeXJlcCBxeiByYW5rIHJhbmtpbmR4IHJlYWRyICcgK1xuICAgICAgICAgICAgICAncmVhbCByZWNsYXNzaWZ5IHJlY2xhc3NpZnlDdXRzIHJlY29kZSByZWNzZXJhciByZWNzZXJjcCByZWNzZXJyYyByZXJ1biByZXNjYWxlIHJlc2hhcGUgcmV0cyByZXYgcmZmdCByZmZ0aSByZmZ0aXAgcmZmdG4gJyArXG4gICAgICAgICAgICAgICdyZmZ0bnAgcmZmdHAgcm5kQmVybm91bGxpIHJuZEJldGEgcm5kQmlub21pYWwgcm5kQ2F1Y2h5IHJuZENoaVNxdWFyZSBybmRDb24gcm5kQ3JlYXRlU3RhdGUgcm5kRXhwIHJuZEdhbW1hIHJuZEdlbyBybmRHdW1iZWwgJyArXG4gICAgICAgICAgICAgICdybmRIeXBlckdlbyBybmRpIHJuZEtNYmV0YSBybmRLTWdhbSBybmRLTWkgcm5kS01uIHJuZEtNbmIgcm5kS01wIHJuZEtNdSBybmRLTXZtIHJuZExhcGxhY2Ugcm5kTENiZXRhIHJuZExDZ2FtIHJuZExDaSBybmRMQ24gJyArXG4gICAgICAgICAgICAgICdybmRMQ25iIHJuZExDcCBybmRMQ3Ugcm5kTEN2bSBybmRMb2dOb3JtIHJuZE1UdSBybmRNVm4gcm5kTVZ0IHJuZG4gcm5kbmIgcm5kTmVnQmlub21pYWwgcm5kcCBybmRQb2lzc29uIHJuZFJheWxlaWdoICcgK1xuICAgICAgICAgICAgICAncm5kU3RhdGVTa2lwIHJuZHUgcm5kdm0gcm5kV2VpYnVsbCBybmRXaXNoYXJ0IHJvdGF0ZXIgcm91bmQgcm93cyByb3dzZiBycmVmIHNhbXBsZURhdGEgc2F0b3N0ckMgc2F2ZWQgc2F2ZVN0cnVjdCBzYXZld2luZCAnICtcbiAgICAgICAgICAgICAgJ3NjYWxlIHNjYWxlM2Qgc2NhbGVyciBzY2FsaW5mbmFubWlzcyBzY2FsbWlzcyBzY2h0b2Mgc2NodXIgc2VhcmNoc291cmNlcGF0aCBzZWVrciBzZWxlY3Qgc2VsaWYgc2VxYSBzZXFtIHNldGRpZiBzZXRkaWZzYSAnICtcbiAgICAgICAgICAgICAgJ3NldHZhcnMgc2V0dndybW9kZSBzZXR3aW5kIHNoZWxsIHNoaWZ0ciBzaW4gc2luZ2xlaW5kZXggc2luaCBzbGVlcCBzb2xwZCBzb3J0YyBzb3J0Y2Mgc29ydGQgc29ydGhjIHNvcnRoY2Mgc29ydGluZCAnICtcbiAgICAgICAgICAgICAgJ3NvcnRpbmRjIHNvcnRtYyBzb3J0ciBzb3J0cmMgc3BCaWNvbmpHcmFkU29sIHNwQ2hvbCBzcENvbmpHcmFkU29sIHNwQ3JlYXRlIHNwRGVuc2VTdWJtYXQgc3BEaWFnUnZNYXQgc3BFaWd2IHNwRXllIHNwTERMICcgK1xuICAgICAgICAgICAgICAnc3BsaW5lIHNwTFUgc3BOdW1OWkUgc3BPbmVzIHNwcmVhZFNoZWV0UmVhZE0gc3ByZWFkU2hlZXRSZWFkU0Egc3ByZWFkU2hlZXRXcml0ZSBzcFNjYWxlIHNwU3VibWF0IHNwVG9EZW5zZSBzcFRyVERlbnNlICcgK1xuICAgICAgICAgICAgICAnc3BUU2NhbGFyIHNwWmVyb3Mgc3FwU29sdmUgc3FwU29sdmVNVCBzcXBTb2x2ZU1UQ29udHJvbENyZWF0ZSBzcXBTb2x2ZU1UbGFncmFuZ2VDcmVhdGUgc3FwU29sdmVNVG91dENyZWF0ZSBzcXBTb2x2ZVNldCAnICtcbiAgICAgICAgICAgICAgJ3NxcnQgc3RhdGVtZW50cyBzdGRjIHN0ZHNjIHN0b2N2IHN0b2Ygc3RyY29tYmluZSBzdHJpbmR4IHN0cmxlbiBzdHJwdXQgc3RycmluZHggc3Ryc2VjdCBzdHJzcGxpdCBzdHJzcGxpdFBhZCBzdHJ0b2R0ICcgK1xuICAgICAgICAgICAgICAnc3RydG9mIHN0cnRvZmNwbHggc3RydHJpbWwgc3RydHJpbXIgc3RydHJ1bmMgc3RydHJ1bmNsIHN0cnRydW5jcGFkIHN0cnRydW5jciBzdWJtYXQgc3Vic2NhdCBzdWJzdHV0ZSBzdWJ2ZWMgc3VtYyBzdW1yICcgK1xuICAgICAgICAgICAgICAnc3VyZmFjZSBzdmQgc3ZkMSBzdmQyIHN2ZGN1c3Ygc3ZkcyBzdmR1c3Ygc3lzc3RhdGUgdGFiIHRhbiB0YW5oIHRlbXBuYW1lICcgK1xuICAgICAgICAgICAgICAndGltZSB0aW1lZHQgdGltZXN0ciB0aW1ldXRjIHRpdGxlIHRrZjJlcHMgdGtmMnBzIHRvY2FydCB0b2RheWR0IHRvZXBsaXR6IHRva2VuIHRvcG9sYXIgdHJhcGNoayAnICtcbiAgICAgICAgICAgICAgJ3RyaWdhbW1hIHRyaW1yIHRydW5jIHR5cGUgdHlwZWN2IHR5cGVmIHVuaW9uIHVuaW9uc2EgdW5pcWluZHggdW5pcWluZHhzYSB1bmlxdWUgdW5pcXVlc2EgdXBtYXQgdXBtYXQxIHVwcGVyIHV0Y3RvZHQgJyArXG4gICAgICAgICAgICAgICd1dGN0b2R0diB1dHJpc29sIHZhbHMgdmFyQ292TVMgdmFyQ292WFMgdmFyZ2V0IHZhcmdldGwgdmFybWFsbCB2YXJtYXJlcyB2YXJwdXQgdmFycHV0bCB2YXJ0eXBlZiB2Y20gdmNtcyB2Y3ggdmN4cyAnICtcbiAgICAgICAgICAgICAgJ3ZlYyB2ZWNoIHZlY3IgdmVjdG9yIHZnZXQgdmlldyB2aWV3eHl6IHZsaXN0IHZuYW1lY3Ygdm9sdW1lIHZwdXQgdnJlYWQgdnR5cGVjdiB3YWl0IHdhaXRjIHdhbGtpbmRleCB3aGVyZSB3aW5kb3cgJyArXG4gICAgICAgICAgICAgICd3cml0ZXIgeGxhYmVsIHhsc0dldFNoZWV0Q291bnQgeGxzR2V0U2hlZXRTaXplIHhsc0dldFNoZWV0VHlwZXMgeGxzTWFrZVJhbmdlIHhsc1JlYWRNIHhsc1JlYWRTQSB4bHNXcml0ZSB4bHNXcml0ZU0gJyArXG4gICAgICAgICAgICAgICd4bHNXcml0ZVNBIHhwbmQgeHRpY3MgeHkgeHl6IHlsYWJlbCB5dGljcyB6ZXJvcyB6ZXRhIHpsYWJlbCB6dGljcyBjZGZFbXBpcmljYWwgZG90IGg1Y3JlYXRlIGg1b3BlbiBoNXJlYWQgaDVyZWFkQXR0cmlidXRlICcgK1xuICAgICAgICAgICAgICAnaDV3cml0ZSBoNXdyaXRlQXR0cmlidXRlIGxkbCBwbG90QWRkRXJyb3JCYXIgcGxvdEFkZFN1cmZhY2UgcGxvdENERkVtcGlyaWNhbCBwbG90U2V0Q29sb3JtYXAgcGxvdFNldENvbnRvdXJMYWJlbHMgJyArXG4gICAgICAgICAgICAgICdwbG90U2V0TGVnZW5kRm9udCBwbG90U2V0VGV4dEludGVycHJldGVyIHBsb3RTZXRYVGljQ291bnQgcGxvdFNldFlUaWNDb3VudCBwbG90U2V0WkxldmVscyBwb3dlcm0gc3Ryam9pbiBzeWx2ZXN0ZXIgJyArXG4gICAgICAgICAgICAgICdzdHJ0cmltJyxcbiAgICBsaXRlcmFsOiAnREJfQUZURVJfTEFTVF9ST1cgREJfQUxMX1RBQkxFUyBEQl9CQVRDSF9PUEVSQVRJT05TIERCX0JFRk9SRV9GSVJTVF9ST1cgREJfQkxPQiBEQl9FVkVOVF9OT1RJRklDQVRJT05TICcgK1xuICAgICAgICAgICAgICdEQl9GSU5JU0hfUVVFUlkgREJfSElHSF9QUkVDSVNJT04gREJfTEFTVF9JTlNFUlRfSUQgREJfTE9XX1BSRUNJU0lPTl9ET1VCTEUgREJfTE9XX1BSRUNJU0lPTl9JTlQzMiAnICtcbiAgICAgICAgICAgICAnREJfTE9XX1BSRUNJU0lPTl9JTlQ2NCBEQl9MT1dfUFJFQ0lTSU9OX05VTUJFUlMgREJfTVVMVElQTEVfUkVTVUxUX1NFVFMgREJfTkFNRURfUExBQ0VIT0xERVJTICcgK1xuICAgICAgICAgICAgICdEQl9QT1NJVElPTkFMX1BMQUNFSE9MREVSUyBEQl9QUkVQQVJFRF9RVUVSSUVTIERCX1FVRVJZX1NJWkUgREJfU0lNUExFX0xPQ0tJTkcgREJfU1lTVEVNX1RBQkxFUyBEQl9UQUJMRVMgJyArXG4gICAgICAgICAgICAgJ0RCX1RSQU5TQUNUSU9OUyBEQl9VTklDT0RFIERCX1ZJRVdTIF9fU1RESU4gX19TVERPVVQgX19TVERFUlIgX19GSUxFX0RJUidcbiAgfTtcblxuICBjb25zdCBBVF9DT01NRU5UX01PREUgPSBobGpzLkNPTU1FTlQoJ0AnLCAnQCcpO1xuXG4gIGNvbnN0IFBSRVBST0NFU1NPUiA9XG4gIHtcbiAgICBjbGFzc05hbWU6ICdtZXRhJyxcbiAgICBiZWdpbjogJyMnLFxuICAgIGVuZDogJyQnLFxuICAgIGtleXdvcmRzOiB7XG4gICAgICAnbWV0YS1rZXl3b3JkJzogJ2RlZmluZSBkZWZpbmVjc3wxMCB1bmRlZiBpZmRlZiBpZm5kZWYgaWZsaWdodCBpZmRsbGNhbGwgaWZtYWMgaWZvczJ3aW4gaWZ1bml4IGVsc2UgZW5kaWYgbGluZXNvbiBsaW5lc29mZiBzcmNmaWxlIHNyY2xpbmUnXG4gICAgfSxcbiAgICBjb250YWluczogW1xuICAgICAge1xuICAgICAgICBiZWdpbjogL1xcXFxcXG4vLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luS2V5d29yZHM6ICdpbmNsdWRlJyxcbiAgICAgICAgZW5kOiAnJCcsXG4gICAgICAgIGtleXdvcmRzOiB7XG4gICAgICAgICAgJ21ldGEta2V5d29yZCc6ICdpbmNsdWRlJ1xuICAgICAgICB9LFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGNsYXNzTmFtZTogJ21ldGEtc3RyaW5nJyxcbiAgICAgICAgICAgIGJlZ2luOiAnXCInLFxuICAgICAgICAgICAgZW5kOiAnXCInLFxuICAgICAgICAgICAgaWxsZWdhbDogJ1xcXFxuJ1xuICAgICAgICAgIH1cbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIGhsanMuQ19MSU5FX0NPTU1FTlRfTU9ERSxcbiAgICAgIGhsanMuQ19CTE9DS19DT01NRU5UX01PREUsXG4gICAgICBBVF9DT01NRU5UX01PREVcbiAgICBdXG4gIH07XG5cbiAgY29uc3QgU1RSVUNUX1RZUEUgPVxuICB7XG4gICAgYmVnaW46IC9cXGJzdHJ1Y3RcXHMrLyxcbiAgICBlbmQ6IC9cXHMvLFxuICAgIGtleXdvcmRzOiBcInN0cnVjdFwiLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogXCJ0eXBlXCIsXG4gICAgICAgIGJlZ2luOiBobGpzLlVOREVSU0NPUkVfSURFTlRfUkUsXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfVxuICAgIF1cbiAgfTtcblxuICAvLyBvbmx5IGZvciBkZWZpbml0aW9uc1xuICBjb25zdCBQQVJTRV9QQVJBTVMgPSBbXG4gICAge1xuICAgICAgY2xhc3NOYW1lOiAncGFyYW1zJyxcbiAgICAgIGJlZ2luOiAvXFwoLyxcbiAgICAgIGVuZDogL1xcKS8sXG4gICAgICBleGNsdWRlQmVnaW46IHRydWUsXG4gICAgICBleGNsdWRlRW5kOiB0cnVlLFxuICAgICAgZW5kc1dpdGhQYXJlbnQ6IHRydWUsXG4gICAgICByZWxldmFuY2U6IDAsXG4gICAgICBjb250YWluczogW1xuICAgICAgICB7IC8vIGRvdHNcbiAgICAgICAgICBjbGFzc05hbWU6ICdsaXRlcmFsJyxcbiAgICAgICAgICBiZWdpbjogL1xcLlxcLlxcLi9cbiAgICAgICAgfSxcbiAgICAgICAgaGxqcy5DX05VTUJFUl9NT0RFLFxuICAgICAgICBobGpzLkNfQkxPQ0tfQ09NTUVOVF9NT0RFLFxuICAgICAgICBBVF9DT01NRU5UX01PREUsXG4gICAgICAgIFNUUlVDVF9UWVBFXG4gICAgICBdXG4gICAgfVxuICBdO1xuXG4gIGNvbnN0IEZVTkNUSU9OX0RFRiA9XG4gIHtcbiAgICBjbGFzc05hbWU6IFwidGl0bGVcIixcbiAgICBiZWdpbjogaGxqcy5VTkRFUlNDT1JFX0lERU5UX1JFLFxuICAgIHJlbGV2YW5jZTogMFxuICB9O1xuXG4gIGNvbnN0IERFRklOSVRJT04gPSBmdW5jdGlvbihiZWdpbktleXdvcmRzLCBlbmQsIGluaGVyaXRzKSB7XG4gICAgY29uc3QgbW9kZSA9IGhsanMuaW5oZXJpdChcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiBcImZ1bmN0aW9uXCIsXG4gICAgICAgIGJlZ2luS2V5d29yZHM6IGJlZ2luS2V5d29yZHMsXG4gICAgICAgIGVuZDogZW5kLFxuICAgICAgICBleGNsdWRlRW5kOiB0cnVlLFxuICAgICAgICBjb250YWluczogW10uY29uY2F0KFBBUlNFX1BBUkFNUylcbiAgICAgIH0sXG4gICAgICBpbmhlcml0cyB8fCB7fVxuICAgICk7XG4gICAgbW9kZS5jb250YWlucy5wdXNoKEZVTkNUSU9OX0RFRik7XG4gICAgbW9kZS5jb250YWlucy5wdXNoKGhsanMuQ19OVU1CRVJfTU9ERSk7XG4gICAgbW9kZS5jb250YWlucy5wdXNoKGhsanMuQ19CTE9DS19DT01NRU5UX01PREUpO1xuICAgIG1vZGUuY29udGFpbnMucHVzaChBVF9DT01NRU5UX01PREUpO1xuICAgIHJldHVybiBtb2RlO1xuICB9O1xuXG4gIGNvbnN0IEJVSUxUX0lOX1JFRiA9XG4gIHsgLy8gdGhlc2UgYXJlIGV4cGxpY2l0bHkgbmFtZWQgaW50ZXJuYWwgZnVuY3Rpb24gY2FsbHNcbiAgICBjbGFzc05hbWU6ICdidWlsdF9pbicsXG4gICAgYmVnaW46ICdcXFxcYignICsgS0VZV09SRFMuYnVpbHRfaW4uc3BsaXQoJyAnKS5qb2luKCd8JykgKyAnKVxcXFxiJ1xuICB9O1xuXG4gIGNvbnN0IFNUUklOR19SRUYgPVxuICB7XG4gICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICBiZWdpbjogJ1wiJyxcbiAgICBlbmQ6ICdcIicsXG4gICAgY29udGFpbnM6IFtobGpzLkJBQ0tTTEFTSF9FU0NBUEVdLFxuICAgIHJlbGV2YW5jZTogMFxuICB9O1xuXG4gIGNvbnN0IEZVTkNUSU9OX1JFRiA9XG4gIHtcbiAgICAvLyBjbGFzc05hbWU6IFwiZm5fcmVmXCIsXG4gICAgYmVnaW46IGhsanMuVU5ERVJTQ09SRV9JREVOVF9SRSArICdcXFxccypcXFxcKCcsXG4gICAgcmV0dXJuQmVnaW46IHRydWUsXG4gICAga2V5d29yZHM6IEtFWVdPUkRTLFxuICAgIHJlbGV2YW5jZTogMCxcbiAgICBjb250YWluczogW1xuICAgICAge1xuICAgICAgICBiZWdpbktleXdvcmRzOiBLRVlXT1JEUy5rZXl3b3JkXG4gICAgICB9LFxuICAgICAgQlVJTFRfSU5fUkVGLFxuICAgICAgeyAvLyBhbWJpZ3VvdXNseSBuYW1lZCBmdW5jdGlvbiBjYWxscyBnZXQgYSByZWxldmFuY2Ugb2YgMFxuICAgICAgICBjbGFzc05hbWU6ICdidWlsdF9pbicsXG4gICAgICAgIGJlZ2luOiBobGpzLlVOREVSU0NPUkVfSURFTlRfUkUsXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfVxuICAgIF1cbiAgfTtcblxuICBjb25zdCBGVU5DVElPTl9SRUZfUEFSQU1TID1cbiAge1xuICAgIC8vIGNsYXNzTmFtZTogXCJmbl9yZWZfcGFyYW1zXCIsXG4gICAgYmVnaW46IC9cXCgvLFxuICAgIGVuZDogL1xcKS8sXG4gICAgcmVsZXZhbmNlOiAwLFxuICAgIGtleXdvcmRzOiB7XG4gICAgICBidWlsdF9pbjogS0VZV09SRFMuYnVpbHRfaW4sXG4gICAgICBsaXRlcmFsOiBLRVlXT1JEUy5saXRlcmFsXG4gICAgfSxcbiAgICBjb250YWluczogW1xuICAgICAgaGxqcy5DX05VTUJFUl9NT0RFLFxuICAgICAgaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERSxcbiAgICAgIEFUX0NPTU1FTlRfTU9ERSxcbiAgICAgIEJVSUxUX0lOX1JFRixcbiAgICAgIEZVTkNUSU9OX1JFRixcbiAgICAgIFNUUklOR19SRUYsXG4gICAgICAnc2VsZidcbiAgICBdXG4gIH07XG5cbiAgRlVOQ1RJT05fUkVGLmNvbnRhaW5zLnB1c2goRlVOQ1RJT05fUkVGX1BBUkFNUyk7XG5cbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnR0FVU1MnLFxuICAgIGFsaWFzZXM6IFsnZ3NzJ10sXG4gICAgY2FzZV9pbnNlbnNpdGl2ZTogdHJ1ZSwgLy8gbGFuZ3VhZ2UgaXMgY2FzZS1pbnNlbnNpdGl2ZVxuICAgIGtleXdvcmRzOiBLRVlXT1JEUyxcbiAgICBpbGxlZ2FsOiAvKFxce1slI118WyUjXVxcfXwgPC0gKS8sXG4gICAgY29udGFpbnM6IFtcbiAgICAgIGhsanMuQ19OVU1CRVJfTU9ERSxcbiAgICAgIGhsanMuQ19MSU5FX0NPTU1FTlRfTU9ERSxcbiAgICAgIGhsanMuQ19CTE9DS19DT01NRU5UX01PREUsXG4gICAgICBBVF9DT01NRU5UX01PREUsXG4gICAgICBTVFJJTkdfUkVGLFxuICAgICAgUFJFUFJPQ0VTU09SLFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdrZXl3b3JkJyxcbiAgICAgICAgYmVnaW46IC9cXGJleHRlcm5hbCAobWF0cml4fHN0cmluZ3xhcnJheXxzcGFyc2UgbWF0cml4fHN0cnVjdHxwcm9jfGtleXdvcmR8Zm4pL1xuICAgICAgfSxcbiAgICAgIERFRklOSVRJT04oJ3Byb2Mga2V5d29yZCcsICc7JyksXG4gICAgICBERUZJTklUSU9OKCdmbicsICc9JyksXG4gICAgICB7XG4gICAgICAgIGJlZ2luS2V5d29yZHM6ICdmb3IgdGhyZWFkZm9yJyxcbiAgICAgICAgZW5kOiAvOy8sXG4gICAgICAgIC8vIGVuZDogL1xcKC8sXG4gICAgICAgIHJlbGV2YW5jZTogMCxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICBobGpzLkNfQkxPQ0tfQ09NTUVOVF9NT0RFLFxuICAgICAgICAgIEFUX0NPTU1FTlRfTU9ERSxcbiAgICAgICAgICBGVU5DVElPTl9SRUZfUEFSQU1TXG4gICAgICAgIF1cbiAgICAgIH0sXG4gICAgICB7IC8vIGN1c3RvbSBtZXRob2QgZ3VhcmRcbiAgICAgICAgLy8gZXhjbHVkZXMgbWV0aG9kIG5hbWVzIGZyb20ga2V5d29yZCBwcm9jZXNzaW5nXG4gICAgICAgIHZhcmlhbnRzOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgYmVnaW46IGhsanMuVU5ERVJTQ09SRV9JREVOVF9SRSArICdcXFxcLicgKyBobGpzLlVOREVSU0NPUkVfSURFTlRfUkVcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiBobGpzLlVOREVSU0NPUkVfSURFTlRfUkUgKyAnXFxcXHMqPSdcbiAgICAgICAgICB9XG4gICAgICAgIF0sXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfSxcbiAgICAgIEZVTkNUSU9OX1JFRixcbiAgICAgIFNUUlVDVF9UWVBFXG4gICAgXVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IGdhdXNzO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9