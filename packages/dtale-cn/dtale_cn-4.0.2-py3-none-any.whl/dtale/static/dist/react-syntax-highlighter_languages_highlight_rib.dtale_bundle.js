(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_rib"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/rib.js":
/*!**********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/rib.js ***!
  \**********************************************************************************************/
/***/ ((module) => {

/*
Language: RenderMan RIB
Author: Konstantin Evdokimenko <qewerty@gmail.com>
Contributors: Shuen-Huei Guan <drake.guan@gmail.com>
Website: https://renderman.pixar.com/resources/RenderMan_20/ribBinding.html
Category: graphics
*/

function rib(hljs) {
  return {
    name: 'RenderMan RIB',
    keywords:
      'ArchiveRecord AreaLightSource Atmosphere Attribute AttributeBegin AttributeEnd Basis ' +
      'Begin Blobby Bound Clipping ClippingPlane Color ColorSamples ConcatTransform Cone ' +
      'CoordinateSystem CoordSysTransform CropWindow Curves Cylinder DepthOfField Detail ' +
      'DetailRange Disk Displacement Display End ErrorHandler Exposure Exterior Format ' +
      'FrameAspectRatio FrameBegin FrameEnd GeneralPolygon GeometricApproximation Geometry ' +
      'Hider Hyperboloid Identity Illuminate Imager Interior LightSource ' +
      'MakeCubeFaceEnvironment MakeLatLongEnvironment MakeShadow MakeTexture Matte ' +
      'MotionBegin MotionEnd NuPatch ObjectBegin ObjectEnd ObjectInstance Opacity Option ' +
      'Orientation Paraboloid Patch PatchMesh Perspective PixelFilter PixelSamples ' +
      'PixelVariance Points PointsGeneralPolygons PointsPolygons Polygon Procedural Projection ' +
      'Quantize ReadArchive RelativeDetail ReverseOrientation Rotate Scale ScreenWindow ' +
      'ShadingInterpolation ShadingRate Shutter Sides Skew SolidBegin SolidEnd Sphere ' +
      'SubdivisionMesh Surface TextureCoordinates Torus Transform TransformBegin TransformEnd ' +
      'TransformPoints Translate TrimCurve WorldBegin WorldEnd',
    illegal: '</',
    contains: [
      hljs.HASH_COMMENT_MODE,
      hljs.C_NUMBER_MODE,
      hljs.APOS_STRING_MODE,
      hljs.QUOTE_STRING_MODE
    ]
  };
}

module.exports = rib;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfcmliLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvcmliLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogUmVuZGVyTWFuIFJJQlxuQXV0aG9yOiBLb25zdGFudGluIEV2ZG9raW1lbmtvIDxxZXdlcnR5QGdtYWlsLmNvbT5cbkNvbnRyaWJ1dG9yczogU2h1ZW4tSHVlaSBHdWFuIDxkcmFrZS5ndWFuQGdtYWlsLmNvbT5cbldlYnNpdGU6IGh0dHBzOi8vcmVuZGVybWFuLnBpeGFyLmNvbS9yZXNvdXJjZXMvUmVuZGVyTWFuXzIwL3JpYkJpbmRpbmcuaHRtbFxuQ2F0ZWdvcnk6IGdyYXBoaWNzXG4qL1xuXG5mdW5jdGlvbiByaWIoaGxqcykge1xuICByZXR1cm4ge1xuICAgIG5hbWU6ICdSZW5kZXJNYW4gUklCJyxcbiAgICBrZXl3b3JkczpcbiAgICAgICdBcmNoaXZlUmVjb3JkIEFyZWFMaWdodFNvdXJjZSBBdG1vc3BoZXJlIEF0dHJpYnV0ZSBBdHRyaWJ1dGVCZWdpbiBBdHRyaWJ1dGVFbmQgQmFzaXMgJyArXG4gICAgICAnQmVnaW4gQmxvYmJ5IEJvdW5kIENsaXBwaW5nIENsaXBwaW5nUGxhbmUgQ29sb3IgQ29sb3JTYW1wbGVzIENvbmNhdFRyYW5zZm9ybSBDb25lICcgK1xuICAgICAgJ0Nvb3JkaW5hdGVTeXN0ZW0gQ29vcmRTeXNUcmFuc2Zvcm0gQ3JvcFdpbmRvdyBDdXJ2ZXMgQ3lsaW5kZXIgRGVwdGhPZkZpZWxkIERldGFpbCAnICtcbiAgICAgICdEZXRhaWxSYW5nZSBEaXNrIERpc3BsYWNlbWVudCBEaXNwbGF5IEVuZCBFcnJvckhhbmRsZXIgRXhwb3N1cmUgRXh0ZXJpb3IgRm9ybWF0ICcgK1xuICAgICAgJ0ZyYW1lQXNwZWN0UmF0aW8gRnJhbWVCZWdpbiBGcmFtZUVuZCBHZW5lcmFsUG9seWdvbiBHZW9tZXRyaWNBcHByb3hpbWF0aW9uIEdlb21ldHJ5ICcgK1xuICAgICAgJ0hpZGVyIEh5cGVyYm9sb2lkIElkZW50aXR5IElsbHVtaW5hdGUgSW1hZ2VyIEludGVyaW9yIExpZ2h0U291cmNlICcgK1xuICAgICAgJ01ha2VDdWJlRmFjZUVudmlyb25tZW50IE1ha2VMYXRMb25nRW52aXJvbm1lbnQgTWFrZVNoYWRvdyBNYWtlVGV4dHVyZSBNYXR0ZSAnICtcbiAgICAgICdNb3Rpb25CZWdpbiBNb3Rpb25FbmQgTnVQYXRjaCBPYmplY3RCZWdpbiBPYmplY3RFbmQgT2JqZWN0SW5zdGFuY2UgT3BhY2l0eSBPcHRpb24gJyArXG4gICAgICAnT3JpZW50YXRpb24gUGFyYWJvbG9pZCBQYXRjaCBQYXRjaE1lc2ggUGVyc3BlY3RpdmUgUGl4ZWxGaWx0ZXIgUGl4ZWxTYW1wbGVzICcgK1xuICAgICAgJ1BpeGVsVmFyaWFuY2UgUG9pbnRzIFBvaW50c0dlbmVyYWxQb2x5Z29ucyBQb2ludHNQb2x5Z29ucyBQb2x5Z29uIFByb2NlZHVyYWwgUHJvamVjdGlvbiAnICtcbiAgICAgICdRdWFudGl6ZSBSZWFkQXJjaGl2ZSBSZWxhdGl2ZURldGFpbCBSZXZlcnNlT3JpZW50YXRpb24gUm90YXRlIFNjYWxlIFNjcmVlbldpbmRvdyAnICtcbiAgICAgICdTaGFkaW5nSW50ZXJwb2xhdGlvbiBTaGFkaW5nUmF0ZSBTaHV0dGVyIFNpZGVzIFNrZXcgU29saWRCZWdpbiBTb2xpZEVuZCBTcGhlcmUgJyArXG4gICAgICAnU3ViZGl2aXNpb25NZXNoIFN1cmZhY2UgVGV4dHVyZUNvb3JkaW5hdGVzIFRvcnVzIFRyYW5zZm9ybSBUcmFuc2Zvcm1CZWdpbiBUcmFuc2Zvcm1FbmQgJyArXG4gICAgICAnVHJhbnNmb3JtUG9pbnRzIFRyYW5zbGF0ZSBUcmltQ3VydmUgV29ybGRCZWdpbiBXb3JsZEVuZCcsXG4gICAgaWxsZWdhbDogJzwvJyxcbiAgICBjb250YWluczogW1xuICAgICAgaGxqcy5IQVNIX0NPTU1FTlRfTU9ERSxcbiAgICAgIGhsanMuQ19OVU1CRVJfTU9ERSxcbiAgICAgIGhsanMuQVBPU19TVFJJTkdfTU9ERSxcbiAgICAgIGhsanMuUVVPVEVfU1RSSU5HX01PREVcbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gcmliO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9