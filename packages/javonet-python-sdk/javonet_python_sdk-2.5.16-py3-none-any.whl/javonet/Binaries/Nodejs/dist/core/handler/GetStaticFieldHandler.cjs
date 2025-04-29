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
var GetStaticFieldHandler_exports = {};
__export(GetStaticFieldHandler_exports, {
  GetStaticFieldHandler: () => GetStaticFieldHandler
});
module.exports = __toCommonJS(GetStaticFieldHandler_exports);
var import_AbstractHandler = require("./AbstractHandler.cjs");
class GetStaticFieldHandler extends import_AbstractHandler.AbstractHandler {
  constructor() {
    super();
    __publicField(this, "requiredParametersCount", 2);
  }
  process(command) {
    try {
      if (command.payload.length < this.requiredParametersCount) {
        throw new Error("Array Static Field parameters mismatch");
      }
      const { payload } = command;
      let type = payload[0];
      let field = payload[1];
      let staticField = type[field];
      if (typeof staticField === "undefined") {
        let fields = Object.keys(type);
        let message = `Field ${field} not found in class. Available fields:
`;
        fields.forEach((fieldIter) => {
          message += `${fieldIter}
`;
        });
        throw new Error(message);
      } else {
        return staticField;
      }
    } catch (error) {
      throw this.process_stack_trace(error, this.constructor.name);
    }
  }
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  GetStaticFieldHandler
});
