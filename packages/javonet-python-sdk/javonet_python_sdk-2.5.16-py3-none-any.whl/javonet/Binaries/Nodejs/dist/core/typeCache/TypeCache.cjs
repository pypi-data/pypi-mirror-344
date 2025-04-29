"use strict";
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __defNormalProp = (obj, key, value) => key in obj ? __defProp(obj, key, { enumerable: true, configurable: true, writable: true, value }) : obj[key] = value;
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);
var __publicField = (obj, key, value) => __defNormalProp(obj, typeof key !== "symbol" ? key + "" : key, value);
var TypeCache_exports = {};
__export(TypeCache_exports, {
  TypeCache: () => TypeCache
});
module.exports = __toCommonJS(TypeCache_exports);
const _TypeCache = class _TypeCache {
  constructor() {
    __publicField(this, "typeCache", []);
    if (_TypeCache._instance === null) {
      _TypeCache._instance = this;
    }
    return _TypeCache._instance;
  }
  cacheType(typRegex) {
    this.typeCache.push(typRegex);
  }
  isTypeCacheEmpty() {
    return this.typeCache.length === 0;
  }
  isTypeAllowed(typeToCheck) {
    for (let pattern of this.typeCache) {
      if (new RegExp(pattern).test(typeToCheck.name)) {
        return true;
      }
    }
    return false;
  }
  getCachedTypes() {
    return this.typeCache;
  }
  clearCache() {
    this.typeCache = [];
    return 0;
  }
};
__publicField(_TypeCache, "_instance", null);
let TypeCache = _TypeCache;
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  TypeCache
});
