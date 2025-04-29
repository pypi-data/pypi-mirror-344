"use strict";
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __typeError = (msg) => {
  throw TypeError(msg);
};
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
var __accessCheck = (obj, member, msg) => member.has(obj) || __typeError("Cannot " + msg);
var __privateGet = (obj, member, getter) => (__accessCheck(obj, member, "read from private field"), getter ? getter.call(obj) : member.get(obj));
var __privateAdd = (obj, member, value) => member.has(obj) ? __typeError("Cannot add the same private member more than once") : member instanceof WeakSet ? member.add(obj) : member.set(obj, value);
var __privateSet = (obj, member, value, setter) => (__accessCheck(obj, member, "write to private field"), setter ? setter.call(obj, value) : member.set(obj, value), value);
var __privateMethod = (obj, member, method) => (__accessCheck(obj, member, "access private method"), method);
var InvocationContext_exports = {};
__export(InvocationContext_exports, {
  InvocationContext: () => InvocationContext,
  InvocationWsContext: () => InvocationWsContext
});
module.exports = __toCommonJS(InvocationContext_exports);
var import_DelegatesCache = require("../core/delegatesCache/DelegatesCache.cjs");
var import_Interpreter = require("../core/interpreter/Interpreter.cjs");
var import_Command = require("../utils/Command.cjs");
var import_CommandType = require("../utils/CommandType.cjs");
var import_ConnectionType = require("../utils/ConnectionType.cjs");
var import_ExceptionThrower = require("../utils/exception/ExceptionThrower.cjs");
var import_RuntimeName = require("../utils/RuntimeName.cjs");
var _a, _runtimeName, _connectionData, _currentCommand, _responseCommand, _interpreter, _isExecuted, _resultValue, _InvocationContext_instances, createInstanceContext_fn, _buildCommand, _encapsulatePayloadItem, _runtimeName2, _connectionData2, _currentCommand2, _responseCommand2, _interpreter2, _isExecuted2, _resultValue2;
_a = Symbol.iterator;
const _InvocationContext = class _InvocationContext {
  constructor(runtimeName, connectionData, command, isExecuted = false) {
    __privateAdd(this, _InvocationContext_instances);
    __privateAdd(this, _runtimeName);
    __privateAdd(this, _connectionData);
    __privateAdd(this, _currentCommand);
    __privateAdd(this, _responseCommand);
    __privateAdd(this, _interpreter);
    // eslint-disable-next-line no-unused-private-class-members
    __privateAdd(this, _isExecuted);
    __privateAdd(this, _resultValue);
    //destructor() {
    //    if (this.#currentCommand.commandType === CommandType.Reference) {
    //        this.#currentCommand = new Command(
    //            this.#runtimeName,
    //            CommandType.DestructReference,
    //            this.#currentCommand.payload
    //        );
    //        this.execute();
    //    }
    //}
    __publicField(this, _a, function() {
      if (__privateGet(this, _currentCommand).commandType !== import_CommandType.CommandType.Reference) {
        throw new Error("Object is not iterable");
      }
      let position = -1;
      let arraySize = this.getSize().execute().getValue();
      return {
        next: () => ({
          value: this.getIndex(++position),
          done: position >= arraySize
        })
      };
    });
    __privateAdd(this, _buildCommand, function(command) {
      for (let i = 0; i < command.payload.length; i++) {
        command.payload[i] = __privateGet(this, _encapsulatePayloadItem).call(this, command.payload[i]);
      }
      return command.prependArgToPayload(__privateGet(this, _currentCommand));
    });
    __privateAdd(this, _encapsulatePayloadItem, function(payloadItem) {
      if (payloadItem instanceof import_Command.Command) {
        for (let i = 0; i < payloadItem.payload.length; i++) {
          payloadItem.payload[i] = __privateGet(this, _encapsulatePayloadItem).call(this, payloadItem.payload[i]);
        }
        return payloadItem;
      } else if (payloadItem instanceof _InvocationContext) {
        return payloadItem.get_current_command();
      } else if (payloadItem instanceof Array) {
        const copiedArray = payloadItem.map((item) => __privateGet(this, _encapsulatePayloadItem).call(this, item));
        return new import_Command.Command(this.runtimeName, import_CommandType.CommandType.Array, copiedArray);
      } else if (typeof payloadItem === "function") {
        let newArray = new Array(payloadItem.length + 1);
        for (let i = 0; i < newArray.length; i++) {
          newArray[i] = typeof Object;
        }
        const args = [import_DelegatesCache.delegatesCacheInstance.addDelegate(payloadItem), import_RuntimeName.RuntimeName.Nodejs].push(
          ...newArray
        );
        return new import_Command.Command(__privateGet(this, _runtimeName), import_CommandType.CommandType.PassDelegate, args);
      } else {
        return new import_Command.Command(this.runtimeName, import_CommandType.CommandType.Value, [payloadItem]);
      }
    });
    __privateSet(this, _runtimeName, runtimeName);
    __privateSet(this, _connectionData, connectionData);
    __privateSet(this, _currentCommand, command);
    __privateSet(this, _responseCommand, null);
    __privateSet(this, _isExecuted, isExecuted);
    __privateSet(this, _interpreter, null);
    __privateSet(this, _resultValue, null);
  }
  get_current_command() {
    return __privateGet(this, _currentCommand);
  }
  /**
   * Executes the current command.
   * Because invocation context is building the intent of executing particular expression on target environment, we call the initial state of invocation context as non-materialized.
   * The non-materialized context wraps either single command or chain of recursively nested commands.
   * Commands are becoming nested through each invocation of methods on Invocation Context.
   * Each invocation triggers the creation of new Invocation Context instance wrapping the current command with new parent command valid for invoked method.
   * Developer can decide on any moment of the materialization for the context taking full control of the chunks of the expression being transferred and processed on target runtime.
   * @returns {InvocationContext} the InvocationContext after executing the command.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/foundations/execute-method)
   * @method
   */
  execute() {
    __privateSet(this, _interpreter, new import_Interpreter.Interpreter());
    __privateSet(this, _responseCommand, __privateGet(this, _interpreter).execute(__privateGet(this, _currentCommand), __privateGet(this, _connectionData)));
    if (__privateGet(this, _responseCommand) === void 0) {
      throw new Error("responseCommand is undefined in Invocation Context execute method");
    }
    if (__privateGet(this, _responseCommand).commandType === import_CommandType.CommandType.Exception) {
      throw import_ExceptionThrower.ExceptionThrower.throwException(__privateGet(this, _responseCommand));
    }
    if (__privateGet(this, _responseCommand).commandType === import_CommandType.CommandType.CreateClassInstance) {
      __privateSet(this, _currentCommand, __privateGet(this, _responseCommand));
      __privateSet(this, _isExecuted, true);
      return this;
    }
    return new _InvocationContext(__privateGet(this, _runtimeName), __privateGet(this, _connectionData), __privateGet(this, _responseCommand), true);
  }
  /**
   * Invokes a static method on the target runtime.
   * @param {string} methodName - The name of the method to invoke.
   * @param {...any} args - Method arguments.
   * @returns {InvocationContext} A new InvocationContext instance that wraps the command to invoke the static method.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/calling-methods/invoking-static-method)
   * @method
   */
  invokeStaticMethod(methodName, ...args) {
    let localCommand = new import_Command.Command(__privateGet(this, _runtimeName), import_CommandType.CommandType.InvokeStaticMethod, [
      methodName,
      ...args
    ]);
    return __privateMethod(this, _InvocationContext_instances, createInstanceContext_fn).call(this, localCommand);
  }
  /**
   * Retrieves the value of a static field from the target runtime.
   * @param {string} fieldName - The name of the field to get.
   * @returns {InvocationContext} A new InvocationContext instance that wraps the command to get the static field.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/fields-and-properties/getting-and-setting-values-for-static-fields-and-properties)
   * @method
   */
  getStaticField(fieldName) {
    let localCommand = new import_Command.Command(__privateGet(this, _runtimeName), import_CommandType.CommandType.GetStaticField, [fieldName]);
    return __privateMethod(this, _InvocationContext_instances, createInstanceContext_fn).call(this, localCommand);
  }
  /**
   * Sets the value of a static field in the target runtime.
   * @param {string} fieldName - The name of the field to set.
   * @param {any} value - The new value of the field.
   * @returns {InvocationContext} A new InvocationContext instance that wraps the command to set the static field.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/fields-and-properties/getting-and-setting-values-for-static-fields-and-properties)
   * @method
   */
  setStaticField(fieldName, value) {
    let localCommand = new import_Command.Command(__privateGet(this, _runtimeName), import_CommandType.CommandType.SetStaticField, [fieldName, value]);
    return __privateMethod(this, _InvocationContext_instances, createInstanceContext_fn).call(this, localCommand);
  }
  /**
   * Creates a new instance of a class in the target runtime.
   * @param {...any} args - The arguments to pass to the class constructor
   * @returns {InvocationContext} A new InvocationContext instance that wraps the command to create the instance.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/calling-methods/creating-instance-and-calling-instance-methods)
   * @method
   */
  createInstance(...args) {
    let localCommand = new import_Command.Command(__privateGet(this, _runtimeName), import_CommandType.CommandType.CreateClassInstance, args);
    return __privateMethod(this, _InvocationContext_instances, createInstanceContext_fn).call(this, localCommand);
  }
  /**
   * Retrieves the value of an instance field from the target runtime.
   * @param {string} fieldName - The name of the field to get.
   * @returns {InvocationContext} A new InvocationContext instance that wraps the command to get the instance field.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/fields-and-properties/getting-and-setting-values-for-instance-fields-and-properties)
   * @method
   */
  getInstanceField(fieldName) {
    let localCommand = new import_Command.Command(__privateGet(this, _runtimeName), import_CommandType.CommandType.GetInstanceField, [fieldName]);
    return __privateMethod(this, _InvocationContext_instances, createInstanceContext_fn).call(this, localCommand);
  }
  /**
   * Sets the value of an instance field in the target runtime.
   * @param {string} fieldName - The name of the field to set.
   * @param {any} value - The new value of the field.
   * @returns {InvocationContext} A new InvocationContext instance that wraps the command to set the instance field.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/fields-and-properties/getting-and-setting-values-for-instance-fields-and-properties)
   * @method
   */
  setInstanceField(fieldName, value) {
    let localCommand = new import_Command.Command(__privateGet(this, _runtimeName), import_CommandType.CommandType.SetInstanceField, [fieldName, value]);
    return __privateMethod(this, _InvocationContext_instances, createInstanceContext_fn).call(this, localCommand);
  }
  /**
   * Invokes an instance method on the target runtime.
   * @param {string} methodName - The name of the method to invoke.
   * @param {...any} args - Method arguments.
   * @returns {InvocationContext} A new InvocationContext instance that wraps the command to invoke the instance method.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/calling-methods/invoking-instance-method)
   * @method
   */
  invokeInstanceMethod(methodName, ...args) {
    let localCommand = new import_Command.Command(__privateGet(this, _runtimeName), import_CommandType.CommandType.InvokeInstanceMethod, [
      methodName,
      ...args
    ]);
    return __privateMethod(this, _InvocationContext_instances, createInstanceContext_fn).call(this, localCommand);
  }
  /**
   * Retrieves the value at a specific index in an array from the target runtime.
   * @param {...any} indexes - the arguments to pass to the array getter. The first argument should be the index.
   * @returns {InvocationContext} A new InvocationContext instance that wraps the command to get the index.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/arrays-and-collections/one-dimensional-arrays)
   * @method
   */
  getIndex(...indexes) {
    let localCommand = new import_Command.Command(__privateGet(this, _runtimeName), import_CommandType.CommandType.ArrayGetItem, indexes);
    return __privateMethod(this, _InvocationContext_instances, createInstanceContext_fn).call(this, localCommand);
  }
  /**
   * Sets the value at a specific index in an array in the target runtime.
   * @param {number[]} indexes - The index to set the value at.
   * @param {any} value - The value to set at the index.
   * @returns {InvocationContext} A new InvocationContext instance that wraps the command to set the index.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/arrays-and-collections/one-dimensional-arrays)
   * @method
   */
  setIndex(indexes, value) {
    let localCommand = new import_Command.Command(__privateGet(this, _runtimeName), import_CommandType.CommandType.ArraySetItem, [indexes, value]);
    return __privateMethod(this, _InvocationContext_instances, createInstanceContext_fn).call(this, localCommand);
  }
  /**
   * Retrieves the size of an array from the target runtime.
   * @returns {InvocationContext} A new InvocationContext instance that wraps the command to get the size.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/arrays-and-collections/one-dimensional-arrays)
   * @method
   */
  getSize() {
    let localCommand = new import_Command.Command(__privateGet(this, _runtimeName), import_CommandType.CommandType.ArrayGetSize, []);
    return __privateMethod(this, _InvocationContext_instances, createInstanceContext_fn).call(this, localCommand);
  }
  /**
   * Retrieves the rank of an array from the target runtime.
   * @returns {InvocationContext} A new InvocationContext instance that wraps the command to get the rank.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/arrays-and-collections/one-dimensional-arrays)
   * @method
   */
  getRank() {
    let localCommand = new import_Command.Command(__privateGet(this, _runtimeName), import_CommandType.CommandType.ArrayGetRank, []);
    return __privateMethod(this, _InvocationContext_instances, createInstanceContext_fn).call(this, localCommand);
  }
  /**
   * Invokes a generic static method on the target runtime.
   * @param {string} methodName - The name of the method to invoke.
   * @param {...any} args - Method arguments.
   * @returns {InvocationContext} A new InvocationContext instance that wraps the command to invoke the generic static method.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/generics/calling-generic-static-method)
   * @method
   */
  invokeGenericStaticMethod(methodName, ...args) {
    let localCommand = new import_Command.Command(__privateGet(this, _runtimeName), import_CommandType.CommandType.InvokeGenericStaticMethod, [
      methodName,
      ...args
    ]);
    return __privateMethod(this, _InvocationContext_instances, createInstanceContext_fn).call(this, localCommand);
  }
  /**
   * Invokes a generic method on the target runtime.
   * @param {string} methodName - The name of the method to invoke.
   * @param {...any} args - Method arguments.
   * @returns {InvocationContext} A new InvocationContext instance that wraps the command to invoke the generic method.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/generics/calling-generic-instance-method)
   * @method
   */
  invokeGenericMethod(methodName, ...args) {
    let localCommand = new import_Command.Command(__privateGet(this, _runtimeName), import_CommandType.CommandType.InvokeGenericMethod, [
      methodName,
      ...args
    ]);
    return __privateMethod(this, _InvocationContext_instances, createInstanceContext_fn).call(this, localCommand);
  }
  /**
   * Retrieves the name of an enum from the target runtime.
   * @returns {InvocationContext} A new InvocationContext instance that wraps the command to get the enum name.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/enums/using-enum-type)
   * @method
   */
  getEnumName() {
    let localCommand = new import_Command.Command(__privateGet(this, _runtimeName), import_CommandType.CommandType.GetEnumName, []);
    return __privateMethod(this, _InvocationContext_instances, createInstanceContext_fn).call(this, localCommand);
  }
  /**
   * Retrieves the value of an enum from the target runtime.
   * @returns {InvocationContext} A new InvocationContext instance that wraps the command to get the enum value.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/enums/using-enum-type)
   * @method
   */
  getEnumValue() {
    let localCommand = new import_Command.Command(__privateGet(this, _runtimeName), import_CommandType.CommandType.GetEnumValue, []);
    return __privateMethod(this, _InvocationContext_instances, createInstanceContext_fn).call(this, localCommand);
  }
  /**
   * Retrieves the value of a reference from the target runtime.
   * @returns {InvocationContext} A new InvocationContext instance that wraps the command to get the ref value.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/methods-arguments/passing-arguments-by-reference-with-ref-keyword)
   * @method
   */
  getRefValue() {
    let localCommand = new import_Command.Command(__privateGet(this, _runtimeName), import_CommandType.CommandType.GetRefValue, []);
    return __privateMethod(this, _InvocationContext_instances, createInstanceContext_fn).call(this, localCommand);
  }
  /**
   * Creates a null object of a specific type on the target runtime.
   *
   * @returns {InvocationContext} An InvocationContext instance with the command to create a null object.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/null-handling/create-null-object)
   * @method
   */
  createNull() {
    let localCommand = new import_Command.Command(__privateGet(this, _runtimeName), import_CommandType.CommandType.CreateNull, []);
    return __privateMethod(this, _InvocationContext_instances, createInstanceContext_fn).call(this, localCommand);
  }
  /**
   * Creates a null object of a specific type on the target runtime.
   * @param {string} methodName - The name of the method to invoke.
   * @param {...any} args - Method arguments.
   * @returns {InvocationContext} An InvocationContext instance with the command to create a null object.
   * TODO: connect documentation page url
   * @see [Javonet Guides](https://www.javonet.com/guides/)
   * @method
   */
  getStaticMethodAsDelegate(methodName, ...args) {
    const localCommand = new import_Command.Command(__privateGet(this, _runtimeName), import_CommandType.CommandType.GetStaticMethodAsDelegate, [
      methodName,
      ...args
    ]);
    return __privateMethod(this, _InvocationContext_instances, createInstanceContext_fn).call(this, localCommand);
  }
  /**
   * Creates a null object of a specific type on the target runtime.
   * @param {string} methodName - The name of the method to invoke.
   * @param {...any} args - Method arguments.
   * @returns {InvocationContext} An InvocationContext instance with the command to create a null object.
   * TODO: connect documentation page url
   * @see [Javonet Guides](https://www.javonet.com/guides/)
   * @method
   */
  getInstanceMethodAsDelegate(methodName, ...args) {
    const localCommand = new import_Command.Command(__privateGet(this, _runtimeName), import_CommandType.CommandType.GetInstanceMethodAsDelegate, [
      methodName,
      ...args
    ]);
    return __privateMethod(this, _InvocationContext_instances, createInstanceContext_fn).call(this, localCommand);
  }
  /**
   * Retrieves an array from the target runtime.
   * @returns {InvocationContext} A new InvocationContext instance that wraps the command to retrieve the array.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/arrays-and-collections/retrieve-array)
   * @method
   */
  retrieveArray() {
    let localCommand = new import_Command.Command(__privateGet(this, _runtimeName), import_CommandType.CommandType.RetrieveArray, []);
    let localInvCtx = new _InvocationContext(
      __privateGet(this, _runtimeName),
      __privateGet(this, _connectionData),
      __privateGet(this, _buildCommand).call(this, localCommand)
    );
    localInvCtx.execute();
    return __privateGet(localInvCtx, _responseCommand).payload;
  }
  /**
   * Returns the primitive value from the target runtime. This could be any primitive type in JavaScript,
   * such as int, boolean, byte, char, long, double, float, etc.
   * @returns {Command} The value of the current command.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/foundations/execute-method)
   * @method
   */
  getValue() {
    __privateSet(this, _resultValue, __privateGet(this, _currentCommand).payload[0]);
    return __privateGet(this, _resultValue);
  }
};
_runtimeName = new WeakMap();
_connectionData = new WeakMap();
_currentCommand = new WeakMap();
_responseCommand = new WeakMap();
_interpreter = new WeakMap();
_isExecuted = new WeakMap();
_resultValue = new WeakMap();
_InvocationContext_instances = new WeakSet();
createInstanceContext_fn = function(localCommand) {
  if (__privateGet(this, _connectionData).connectionType === import_ConnectionType.ConnectionType.WEB_SOCKET) {
    return new InvocationWsContext(
      __privateGet(this, _runtimeName),
      __privateGet(this, _connectionData),
      __privateGet(this, _buildCommand).call(this, localCommand)
    );
  }
  return new _InvocationContext(
    __privateGet(this, _runtimeName),
    __privateGet(this, _connectionData),
    __privateGet(this, _buildCommand).call(this, localCommand)
  );
};
_buildCommand = new WeakMap();
_encapsulatePayloadItem = new WeakMap();
let InvocationContext = _InvocationContext;
const _InvocationWsContext = class _InvocationWsContext extends InvocationContext {
  constructor(runtimeName, connectionData, command, isExecuted = false) {
    super(runtimeName, connectionData, command, isExecuted);
    __privateAdd(this, _runtimeName2);
    __privateAdd(this, _connectionData2);
    __privateAdd(this, _currentCommand2);
    __privateAdd(this, _responseCommand2);
    __privateAdd(this, _interpreter2);
    // eslint-disable-next-line no-unused-private-class-members
    __privateAdd(this, _isExecuted2);
    // eslint-disable-next-line no-unused-private-class-members
    __privateAdd(this, _resultValue2);
    __privateSet(this, _runtimeName2, runtimeName);
    __privateSet(this, _connectionData2, connectionData);
    __privateSet(this, _currentCommand2, command);
    __privateSet(this, _responseCommand2, null);
    __privateSet(this, _isExecuted2, isExecuted);
    __privateSet(this, _interpreter2, null);
    __privateSet(this, _resultValue2, null);
  }
  /**
   * Executes the current command.
   * Because invocation context is building the intent of executing particular expression on target environment, we call the initial state of invocation context as non-materialized.
   * The non-materialized context wraps either single command or chain of recursively nested commands.
   * Commands are becoming nested through each invocation of methods on Invocation Context.
   * Each invocation triggers the creation of new Invocation Context instance wrapping the current command with new parent command valid for invoked method.
   * Developer can decide on any moment of the materialization for the context taking full control of the chunks of the expression being transferred and processed on target runtime.
   * @returns {InvocationContext} the InvocationContext after executing the command.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/foundations/execute-method)
   * @method
   */
  async execute() {
    __privateSet(this, _interpreter2, new import_Interpreter.Interpreter());
    __privateSet(this, _responseCommand2, await __privateGet(this, _interpreter2).executeAsync(
      __privateGet(this, _currentCommand2),
      __privateGet(this, _connectionData2)
    ));
    if (__privateGet(this, _responseCommand2) === void 0) {
      throw new Error("responseCommand is undefined in Invocation Context execute method");
    }
    if (__privateGet(this, _responseCommand2).commandType === import_CommandType.CommandType.Exception) {
      throw import_ExceptionThrower.ExceptionThrower.throwException(__privateGet(this, _responseCommand2));
    }
    if (__privateGet(this, _responseCommand2).commandType === import_CommandType.CommandType.CreateClassInstance) {
      __privateSet(this, _currentCommand2, __privateGet(this, _responseCommand2));
      __privateSet(this, _isExecuted2, true);
      return this;
    }
    return new _InvocationWsContext(__privateGet(this, _runtimeName2), __privateGet(this, _connectionData2), __privateGet(this, _responseCommand2), true);
  }
};
_runtimeName2 = new WeakMap();
_connectionData2 = new WeakMap();
_currentCommand2 = new WeakMap();
_responseCommand2 = new WeakMap();
_interpreter2 = new WeakMap();
_isExecuted2 = new WeakMap();
_resultValue2 = new WeakMap();
let InvocationWsContext = _InvocationWsContext;
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  InvocationContext,
  InvocationWsContext
});
