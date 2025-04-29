"use strict";
var __create = Object.create;
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getProtoOf = Object.getPrototypeOf;
var __hasOwnProp = Object.prototype.hasOwnProperty;
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
var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(
  // If the importer is in node compatibility mode or this is not an ESM
  // file that has been converted to a CommonJS file using a Babel-
  // compatible transform (i.e. "__esModule" has not been set), then set
  // "default" to the CommonJS "module.exports" for node compatibility.
  isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target,
  mod
));
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);
var Runtime_exports = {};
__export(Runtime_exports, {
  getDependency: () => getDependency,
  getDirname: () => getDirname,
  getRequire: () => getRequire,
  getRuntimeExtension: () => getRuntimeExtension,
  isBrowserRuntime: () => isBrowserRuntime,
  isEsmRuntime: () => isEsmRuntime,
  isNodejsRuntime: () => isNodejsRuntime
});
module.exports = __toCommonJS(Runtime_exports);
var import_module = require("module");
var import_path = __toESM(require("path"), 1);
var import_url = require("url");
const import_meta = {};
function isNodejsRuntime() {
  return typeof process !== "undefined" && process.versions != null && process.versions.node != null;
}
function isBrowserRuntime() {
  return typeof window !== "undefined" && typeof window.document !== "undefined";
}
function isEsmRuntime() {
  return typeof __filename === "undefined";
}
function getRuntimeExtension() {
  return isEsmRuntime() ? "js" : "cjs";
}
const getRequire = (callerPath) => {
  try {
    if (isNodejsRuntime()) {
      if (typeof require !== "undefined") {
        return require;
      }
      if (callerPath === void 0) {
        return (0, import_module.createRequire)(import_meta.url);
      }
      const baseUrl = callerPath?.startsWith("file:") ? callerPath : (0, import_url.pathToFileURL)(callerPath).href;
      return (0, import_module.createRequire)(baseUrl);
    }
    return new Error("Runtime not supported");
  } catch (error) {
    throw error;
  }
};
const getDirname = () => {
  if (isEsmRuntime()) {
    const __filename2 = (0, import_url.fileURLToPath)(import_meta.url);
    return import_path.default.dirname(__filename2);
  }
  return __dirname;
};
const getDependency = (dependencyName, callerPathOrUrl) => {
  try {
    let baseUrl = callerPathOrUrl;
    if (!baseUrl && typeof __filename !== "undefined") {
      baseUrl = __filename;
    }
    const contextualRequire = getRequire(baseUrl);
    return contextualRequire.resolve(dependencyName);
  } catch (error) {
    throw new Error(
      `Failed to resolve dependency '${dependencyName}' from '${callerPathOrUrl}': ${error.message}`
    );
  }
};
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  getDependency,
  getDirname,
  getRequire,
  getRuntimeExtension,
  isBrowserRuntime,
  isEsmRuntime,
  isNodejsRuntime
});
