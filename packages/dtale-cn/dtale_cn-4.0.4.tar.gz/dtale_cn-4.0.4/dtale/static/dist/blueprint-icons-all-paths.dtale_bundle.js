"use strict";
(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["blueprint-icons-all-paths"],{

/***/ "./node_modules/@blueprintjs/icons/lib/esm/allPaths.js":
/*!*************************************************************!*\
  !*** ./node_modules/@blueprintjs/icons/lib/esm/allPaths.js ***!
  \*************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   IconSvgPaths16: () => (/* reexport module object */ _generated_16px_paths__WEBPACK_IMPORTED_MODULE_0__),
/* harmony export */   IconSvgPaths20: () => (/* reexport module object */ _generated_20px_paths__WEBPACK_IMPORTED_MODULE_1__),
/* harmony export */   getIconPaths: () => (/* binding */ getIconPaths),
/* harmony export */   iconNameToPathsRecordKey: () => (/* binding */ iconNameToPathsRecordKey)
/* harmony export */ });
/* harmony import */ var change_case__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! change-case */ "./node_modules/pascal-case/dist.es2015/index.js");
/* harmony import */ var _generated_16px_paths__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./generated/16px/paths */ "./node_modules/@blueprintjs/icons/lib/esm/generated/16px/paths/index.js");
/* harmony import */ var _generated_20px_paths__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./generated/20px/paths */ "./node_modules/@blueprintjs/icons/lib/esm/generated/20px/paths/index.js");
/* harmony import */ var _iconTypes__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./iconTypes */ "./node_modules/@blueprintjs/icons/lib/esm/iconTypes.js");
/*
 * Copyright 2021 Palantir Technologies, Inc. All rights reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */





/**
 * Get the list of vector paths that define a given icon. These path strings are used to render `<path>`
 * elements inside an `<svg>` icon element. For full implementation details and nuances, see the icon component
 * handlebars template and `generate-icon-components` script in the __@blueprintjs/icons__ package.
 *
 * Note: this function loads all icon definitions __statically__, which means every icon is included in your
 * JS bundle. Only use this API if your app is likely to use all Blueprint icons at runtime. If you are looking for a
 * dynamic icon loader which loads icon definitions on-demand, use `{ Icons } from "@blueprintjs/icons"` instead.
 */
function getIconPaths(name, size) {
    var key = (0,change_case__WEBPACK_IMPORTED_MODULE_2__.pascalCase)(name);
    return size === _iconTypes__WEBPACK_IMPORTED_MODULE_3__.IconSize.STANDARD ? _generated_16px_paths__WEBPACK_IMPORTED_MODULE_0__[key] : _generated_20px_paths__WEBPACK_IMPORTED_MODULE_1__[key];
}
/**
 * Type safe string literal conversion of snake-case icon names to PascalCase icon names.
 * This is useful for indexing into the SVG paths record to extract a single icon's SVG path definition.
 *
 * @deprecated use `getIconPaths` instead
 */
function iconNameToPathsRecordKey(name) {
    return (0,change_case__WEBPACK_IMPORTED_MODULE_2__.pascalCase)(name);
}
//# sourceMappingURL=allPaths.js.map

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiYmx1ZXByaW50LWljb25zLWFsbC1wYXRocy5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDeUM7QUFDZ0I7QUFDQTtBQUNsQjtBQUNHO0FBQzFDO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0Esc0VBQXNFLFFBQVE7QUFDOUU7QUFDTztBQUNQLGNBQWMsdURBQVU7QUFDeEIsb0JBQW9CLGdEQUFRLFlBQVksa0RBQWMsUUFBUSxrREFBYztBQUM1RTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNPO0FBQ1AsV0FBVyx1REFBVTtBQUNyQjtBQUNBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvQGJsdWVwcmludGpzL2ljb25zL2xpYi9lc20vYWxsUGF0aHMuanMiXSwic291cmNlc0NvbnRlbnQiOlsiLypcbiAqIENvcHlyaWdodCAyMDIxIFBhbGFudGlyIFRlY2hub2xvZ2llcywgSW5jLiBBbGwgcmlnaHRzIHJlc2VydmVkLlxuICpcbiAqIExpY2Vuc2VkIHVuZGVyIHRoZSBBcGFjaGUgTGljZW5zZSwgVmVyc2lvbiAyLjAgKHRoZSBcIkxpY2Vuc2VcIik7XG4gKiB5b3UgbWF5IG5vdCB1c2UgdGhpcyBmaWxlIGV4Y2VwdCBpbiBjb21wbGlhbmNlIHdpdGggdGhlIExpY2Vuc2UuXG4gKiBZb3UgbWF5IG9idGFpbiBhIGNvcHkgb2YgdGhlIExpY2Vuc2UgYXRcbiAqXG4gKiAgICAgaHR0cDovL3d3dy5hcGFjaGUub3JnL2xpY2Vuc2VzL0xJQ0VOU0UtMi4wXG4gKlxuICogVW5sZXNzIHJlcXVpcmVkIGJ5IGFwcGxpY2FibGUgbGF3IG9yIGFncmVlZCB0byBpbiB3cml0aW5nLCBzb2Z0d2FyZVxuICogZGlzdHJpYnV0ZWQgdW5kZXIgdGhlIExpY2Vuc2UgaXMgZGlzdHJpYnV0ZWQgb24gYW4gXCJBUyBJU1wiIEJBU0lTLFxuICogV0lUSE9VVCBXQVJSQU5USUVTIE9SIENPTkRJVElPTlMgT0YgQU5ZIEtJTkQsIGVpdGhlciBleHByZXNzIG9yIGltcGxpZWQuXG4gKiBTZWUgdGhlIExpY2Vuc2UgZm9yIHRoZSBzcGVjaWZpYyBsYW5ndWFnZSBnb3Zlcm5pbmcgcGVybWlzc2lvbnMgYW5kXG4gKiBsaW1pdGF0aW9ucyB1bmRlciB0aGUgTGljZW5zZS5cbiAqL1xuaW1wb3J0IHsgcGFzY2FsQ2FzZSB9IGZyb20gXCJjaGFuZ2UtY2FzZVwiO1xuaW1wb3J0ICogYXMgSWNvblN2Z1BhdGhzMTYgZnJvbSBcIi4vZ2VuZXJhdGVkLzE2cHgvcGF0aHNcIjtcbmltcG9ydCAqIGFzIEljb25TdmdQYXRoczIwIGZyb20gXCIuL2dlbmVyYXRlZC8yMHB4L3BhdGhzXCI7XG5pbXBvcnQgeyBJY29uU2l6ZSB9IGZyb20gXCIuL2ljb25UeXBlc1wiO1xuZXhwb3J0IHsgSWNvblN2Z1BhdGhzMTYsIEljb25TdmdQYXRoczIwIH07XG4vKipcbiAqIEdldCB0aGUgbGlzdCBvZiB2ZWN0b3IgcGF0aHMgdGhhdCBkZWZpbmUgYSBnaXZlbiBpY29uLiBUaGVzZSBwYXRoIHN0cmluZ3MgYXJlIHVzZWQgdG8gcmVuZGVyIGA8cGF0aD5gXG4gKiBlbGVtZW50cyBpbnNpZGUgYW4gYDxzdmc+YCBpY29uIGVsZW1lbnQuIEZvciBmdWxsIGltcGxlbWVudGF0aW9uIGRldGFpbHMgYW5kIG51YW5jZXMsIHNlZSB0aGUgaWNvbiBjb21wb25lbnRcbiAqIGhhbmRsZWJhcnMgdGVtcGxhdGUgYW5kIGBnZW5lcmF0ZS1pY29uLWNvbXBvbmVudHNgIHNjcmlwdCBpbiB0aGUgX19AYmx1ZXByaW50anMvaWNvbnNfXyBwYWNrYWdlLlxuICpcbiAqIE5vdGU6IHRoaXMgZnVuY3Rpb24gbG9hZHMgYWxsIGljb24gZGVmaW5pdGlvbnMgX19zdGF0aWNhbGx5X18sIHdoaWNoIG1lYW5zIGV2ZXJ5IGljb24gaXMgaW5jbHVkZWQgaW4geW91clxuICogSlMgYnVuZGxlLiBPbmx5IHVzZSB0aGlzIEFQSSBpZiB5b3VyIGFwcCBpcyBsaWtlbHkgdG8gdXNlIGFsbCBCbHVlcHJpbnQgaWNvbnMgYXQgcnVudGltZS4gSWYgeW91IGFyZSBsb29raW5nIGZvciBhXG4gKiBkeW5hbWljIGljb24gbG9hZGVyIHdoaWNoIGxvYWRzIGljb24gZGVmaW5pdGlvbnMgb24tZGVtYW5kLCB1c2UgYHsgSWNvbnMgfSBmcm9tIFwiQGJsdWVwcmludGpzL2ljb25zXCJgIGluc3RlYWQuXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBnZXRJY29uUGF0aHMobmFtZSwgc2l6ZSkge1xuICAgIHZhciBrZXkgPSBwYXNjYWxDYXNlKG5hbWUpO1xuICAgIHJldHVybiBzaXplID09PSBJY29uU2l6ZS5TVEFOREFSRCA/IEljb25TdmdQYXRoczE2W2tleV0gOiBJY29uU3ZnUGF0aHMyMFtrZXldO1xufVxuLyoqXG4gKiBUeXBlIHNhZmUgc3RyaW5nIGxpdGVyYWwgY29udmVyc2lvbiBvZiBzbmFrZS1jYXNlIGljb24gbmFtZXMgdG8gUGFzY2FsQ2FzZSBpY29uIG5hbWVzLlxuICogVGhpcyBpcyB1c2VmdWwgZm9yIGluZGV4aW5nIGludG8gdGhlIFNWRyBwYXRocyByZWNvcmQgdG8gZXh0cmFjdCBhIHNpbmdsZSBpY29uJ3MgU1ZHIHBhdGggZGVmaW5pdGlvbi5cbiAqXG4gKiBAZGVwcmVjYXRlZCB1c2UgYGdldEljb25QYXRoc2AgaW5zdGVhZFxuICovXG5leHBvcnQgZnVuY3Rpb24gaWNvbk5hbWVUb1BhdGhzUmVjb3JkS2V5KG5hbWUpIHtcbiAgICByZXR1cm4gcGFzY2FsQ2FzZShuYW1lKTtcbn1cbi8vIyBzb3VyY2VNYXBwaW5nVVJMPWFsbFBhdGhzLmpzLm1hcCJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==