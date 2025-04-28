var Nn = (e) => {
  throw TypeError(e);
};
var Fn = (e, t, n) => t.has(e) || Nn("Cannot " + n);
var ze = (e, t, n) => (Fn(e, t, "read from private field"), n ? n.call(e) : t.get(e)), On = (e, t, n) => t.has(e) ? Nn("Cannot add the same private member more than once") : t instanceof WeakSet ? t.add(e) : t.set(e, n), jn = (e, t, n, r) => (Fn(e, t, "write to private field"), r ? r.call(e, n) : t.set(e, n), n);
import { i as Fo, a as ve, r as Oo, b as jo, w as ft, g as ko, c as j, d as bn, e as mt, o as An } from "./Index-xu1PpPdp.js";
const L = window.ms_globals.React, c = window.ms_globals.React, Po = window.ms_globals.React.isValidElement, Io = window.ms_globals.React.version, J = window.ms_globals.React.useRef, Mo = window.ms_globals.React.useLayoutEffect, _e = window.ms_globals.React.useEffect, Lo = window.ms_globals.React.useCallback, ue = window.ms_globals.React.useMemo, No = window.ms_globals.React.forwardRef, Ze = window.ms_globals.React.useState, kn = window.ms_globals.ReactDOM, ht = window.ms_globals.ReactDOM.createPortal, Ao = window.ms_globals.antdIcons.FileTextFilled, zo = window.ms_globals.antdIcons.CloseCircleFilled, Do = window.ms_globals.antdIcons.FileExcelFilled, Ho = window.ms_globals.antdIcons.FileImageFilled, Bo = window.ms_globals.antdIcons.FileMarkdownFilled, Wo = window.ms_globals.antdIcons.FilePdfFilled, Vo = window.ms_globals.antdIcons.FilePptFilled, Xo = window.ms_globals.antdIcons.FileWordFilled, Uo = window.ms_globals.antdIcons.FileZipFilled, Go = window.ms_globals.antdIcons.PlusOutlined, qo = window.ms_globals.antdIcons.LeftOutlined, Ko = window.ms_globals.antdIcons.RightOutlined, Yo = window.ms_globals.antdIcons.CloseOutlined, Lr = window.ms_globals.antdIcons.CheckOutlined, Qo = window.ms_globals.antdIcons.DeleteOutlined, Zo = window.ms_globals.antdIcons.EditOutlined, Jo = window.ms_globals.antdIcons.SyncOutlined, es = window.ms_globals.antdIcons.DislikeOutlined, ts = window.ms_globals.antdIcons.LikeOutlined, ns = window.ms_globals.antdIcons.CopyOutlined, rs = window.ms_globals.antdIcons.EyeOutlined, os = window.ms_globals.antdIcons.ArrowDownOutlined, ss = window.ms_globals.antd.ConfigProvider, Nr = window.ms_globals.antd.Upload, We = window.ms_globals.antd.theme, is = window.ms_globals.antd.Progress, as = window.ms_globals.antd.Image, se = window.ms_globals.antd.Button, Ee = window.ms_globals.antd.Flex, Te = window.ms_globals.antd.Typography, ls = window.ms_globals.antd.Avatar, cs = window.ms_globals.antd.Popconfirm, us = window.ms_globals.antd.Tooltip, ds = window.ms_globals.antd.Collapse, fs = window.ms_globals.antd.Input, Fr = window.ms_globals.createItemsContext.createItemsContext, ms = window.ms_globals.internalContext.useContextPropsContext, zn = window.ms_globals.internalContext.ContextPropsProvider, Ve = window.ms_globals.antdCssinjs.unit, Wt = window.ms_globals.antdCssinjs.token2CSSVar, Dn = window.ms_globals.antdCssinjs.useStyleRegister, ps = window.ms_globals.antdCssinjs.useCSSVarRegister, gs = window.ms_globals.antdCssinjs.createTheme, hs = window.ms_globals.antdCssinjs.useCacheToken, Or = window.ms_globals.antdCssinjs.Keyframes, yt = window.ms_globals.components.Markdown;
var ys = /\s/;
function vs(e) {
  for (var t = e.length; t-- && ys.test(e.charAt(t)); )
    ;
  return t;
}
var bs = /^\s+/;
function Ss(e) {
  return e && e.slice(0, vs(e) + 1).replace(bs, "");
}
var Hn = NaN, xs = /^[-+]0x[0-9a-f]+$/i, ws = /^0b[01]+$/i, _s = /^0o[0-7]+$/i, Es = parseInt;
function Bn(e) {
  if (typeof e == "number")
    return e;
  if (Fo(e))
    return Hn;
  if (ve(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = ve(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = Ss(e);
  var n = ws.test(e);
  return n || _s.test(e) ? Es(e.slice(2), n ? 2 : 8) : xs.test(e) ? Hn : +e;
}
var Vt = function() {
  return Oo.Date.now();
}, Cs = "Expected a function", Ts = Math.max, $s = Math.min;
function Rs(e, t, n) {
  var r, o, s, i, a, l, u = 0, f = !1, m = !1, d = !0;
  if (typeof e != "function")
    throw new TypeError(Cs);
  t = Bn(t) || 0, ve(n) && (f = !!n.leading, m = "maxWait" in n, s = m ? Ts(Bn(n.maxWait) || 0, t) : s, d = "trailing" in n ? !!n.trailing : d);
  function h(x) {
    var I = r, _ = o;
    return r = o = void 0, u = x, i = e.apply(_, I), i;
  }
  function v(x) {
    return u = x, a = setTimeout(y, t), f ? h(x) : i;
  }
  function g(x) {
    var I = x - l, _ = x - u, P = t - I;
    return m ? $s(P, s - _) : P;
  }
  function p(x) {
    var I = x - l, _ = x - u;
    return l === void 0 || I >= t || I < 0 || m && _ >= s;
  }
  function y() {
    var x = Vt();
    if (p(x))
      return T(x);
    a = setTimeout(y, g(x));
  }
  function T(x) {
    return a = void 0, d && r ? h(x) : (r = o = void 0, i);
  }
  function R() {
    a !== void 0 && clearTimeout(a), u = 0, r = l = o = a = void 0;
  }
  function $() {
    return a === void 0 ? i : T(Vt());
  }
  function E() {
    var x = Vt(), I = p(x);
    if (r = arguments, o = this, l = x, I) {
      if (a === void 0)
        return v(l);
      if (m)
        return clearTimeout(a), a = setTimeout(y, t), h(l);
    }
    return a === void 0 && (a = setTimeout(y, t)), i;
  }
  return E.cancel = R, E.flush = $, E;
}
function Ps(e, t) {
  return jo(e, t);
}
var jr = {
  exports: {}
}, wt = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Is = c, Ms = Symbol.for("react.element"), Ls = Symbol.for("react.fragment"), Ns = Object.prototype.hasOwnProperty, Fs = Is.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Os = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function kr(e, t, n) {
  var r, o = {}, s = null, i = null;
  n !== void 0 && (s = "" + n), t.key !== void 0 && (s = "" + t.key), t.ref !== void 0 && (i = t.ref);
  for (r in t) Ns.call(t, r) && !Os.hasOwnProperty(r) && (o[r] = t[r]);
  if (e && e.defaultProps) for (r in t = e.defaultProps, t) o[r] === void 0 && (o[r] = t[r]);
  return {
    $$typeof: Ms,
    type: e,
    key: s,
    ref: i,
    props: o,
    _owner: Fs.current
  };
}
wt.Fragment = Ls;
wt.jsx = kr;
wt.jsxs = kr;
jr.exports = wt;
var S = jr.exports;
const {
  SvelteComponent: js,
  assign: Wn,
  binding_callbacks: Vn,
  check_outros: ks,
  children: Ar,
  claim_element: zr,
  claim_space: As,
  component_subscribe: Xn,
  compute_slots: zs,
  create_slot: Ds,
  detach: De,
  element: Dr,
  empty: Un,
  exclude_internal_props: Gn,
  get_all_dirty_from_scope: Hs,
  get_slot_changes: Bs,
  group_outros: Ws,
  init: Vs,
  insert_hydration: pt,
  safe_not_equal: Xs,
  set_custom_element_data: Hr,
  space: Us,
  transition_in: gt,
  transition_out: tn,
  update_slot_base: Gs
} = window.__gradio__svelte__internal, {
  beforeUpdate: qs,
  getContext: Ks,
  onDestroy: Ys,
  setContext: Qs
} = window.__gradio__svelte__internal;
function qn(e) {
  let t, n;
  const r = (
    /*#slots*/
    e[7].default
  ), o = Ds(
    r,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = Dr("svelte-slot"), o && o.c(), this.h();
    },
    l(s) {
      t = zr(s, "SVELTE-SLOT", {
        class: !0
      });
      var i = Ar(t);
      o && o.l(i), i.forEach(De), this.h();
    },
    h() {
      Hr(t, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      pt(s, t, i), o && o.m(t, null), e[9](t), n = !0;
    },
    p(s, i) {
      o && o.p && (!n || i & /*$$scope*/
      64) && Gs(
        o,
        r,
        s,
        /*$$scope*/
        s[6],
        n ? Bs(
          r,
          /*$$scope*/
          s[6],
          i,
          null
        ) : Hs(
          /*$$scope*/
          s[6]
        ),
        null
      );
    },
    i(s) {
      n || (gt(o, s), n = !0);
    },
    o(s) {
      tn(o, s), n = !1;
    },
    d(s) {
      s && De(t), o && o.d(s), e[9](null);
    }
  };
}
function Zs(e) {
  let t, n, r, o, s = (
    /*$$slots*/
    e[4].default && qn(e)
  );
  return {
    c() {
      t = Dr("react-portal-target"), n = Us(), s && s.c(), r = Un(), this.h();
    },
    l(i) {
      t = zr(i, "REACT-PORTAL-TARGET", {
        class: !0
      }), Ar(t).forEach(De), n = As(i), s && s.l(i), r = Un(), this.h();
    },
    h() {
      Hr(t, "class", "svelte-1rt0kpf");
    },
    m(i, a) {
      pt(i, t, a), e[8](t), pt(i, n, a), s && s.m(i, a), pt(i, r, a), o = !0;
    },
    p(i, [a]) {
      /*$$slots*/
      i[4].default ? s ? (s.p(i, a), a & /*$$slots*/
      16 && gt(s, 1)) : (s = qn(i), s.c(), gt(s, 1), s.m(r.parentNode, r)) : s && (Ws(), tn(s, 1, 1, () => {
        s = null;
      }), ks());
    },
    i(i) {
      o || (gt(s), o = !0);
    },
    o(i) {
      tn(s), o = !1;
    },
    d(i) {
      i && (De(t), De(n), De(r)), e[8](null), s && s.d(i);
    }
  };
}
function Kn(e) {
  const {
    svelteInit: t,
    ...n
  } = e;
  return n;
}
function Js(e, t, n) {
  let r, o, {
    $$slots: s = {},
    $$scope: i
  } = t;
  const a = zs(s);
  let {
    svelteInit: l
  } = t;
  const u = ft(Kn(t)), f = ft();
  Xn(e, f, ($) => n(0, r = $));
  const m = ft();
  Xn(e, m, ($) => n(1, o = $));
  const d = [], h = Ks("$$ms-gr-react-wrapper"), {
    slotKey: v,
    slotIndex: g,
    subSlotIndex: p
  } = ko() || {}, y = l({
    parent: h,
    props: u,
    target: f,
    slot: m,
    slotKey: v,
    slotIndex: g,
    subSlotIndex: p,
    onDestroy($) {
      d.push($);
    }
  });
  Qs("$$ms-gr-react-wrapper", y), qs(() => {
    u.set(Kn(t));
  }), Ys(() => {
    d.forEach(($) => $());
  });
  function T($) {
    Vn[$ ? "unshift" : "push"](() => {
      r = $, f.set(r);
    });
  }
  function R($) {
    Vn[$ ? "unshift" : "push"](() => {
      o = $, m.set(o);
    });
  }
  return e.$$set = ($) => {
    n(17, t = Wn(Wn({}, t), Gn($))), "svelteInit" in $ && n(5, l = $.svelteInit), "$$scope" in $ && n(6, i = $.$$scope);
  }, t = Gn(t), [r, o, f, m, a, l, i, s, T, R];
}
class ei extends js {
  constructor(t) {
    super(), Vs(this, t, Js, Zs, Xs, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: oc
} = window.__gradio__svelte__internal, Yn = window.ms_globals.rerender, Xt = window.ms_globals.tree;
function ti(e, t = {}) {
  function n(r) {
    const o = ft(), s = new ei({
      ...r,
      props: {
        svelteInit(i) {
          window.ms_globals.autokey += 1;
          const a = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: e,
            props: i.props,
            slot: i.slot,
            target: i.target,
            slotIndex: i.slotIndex,
            subSlotIndex: i.subSlotIndex,
            ignore: t.ignore,
            slotKey: i.slotKey,
            nodes: []
          }, l = i.parent ?? Xt;
          return l.nodes = [...l.nodes, a], Yn({
            createPortal: ht,
            node: Xt
          }), i.onDestroy(() => {
            l.nodes = l.nodes.filter((u) => u.svelteInstance !== o), Yn({
              createPortal: ht,
              node: Xt
            });
          }), a;
        },
        ...r.props
      }
    });
    return o.set(s), s;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(n);
    });
  });
}
const ni = "1.1.0", ri = /* @__PURE__ */ c.createContext({}), oi = {
  classNames: {},
  styles: {},
  className: "",
  style: {}
}, _t = (e) => {
  const t = c.useContext(ri);
  return c.useMemo(() => ({
    ...oi,
    ...t[e]
  }), [t[e]]);
};
function be() {
  return be = Object.assign ? Object.assign.bind() : function(e) {
    for (var t = 1; t < arguments.length; t++) {
      var n = arguments[t];
      for (var r in n) ({}).hasOwnProperty.call(n, r) && (e[r] = n[r]);
    }
    return e;
  }, be.apply(null, arguments);
}
function $e() {
  const {
    getPrefixCls: e,
    direction: t,
    csp: n,
    iconPrefixCls: r,
    theme: o
  } = c.useContext(ss.ConfigContext);
  return {
    theme: o,
    getPrefixCls: e,
    direction: t,
    csp: n,
    iconPrefixCls: r
  };
}
function Re(e) {
  var t = L.useRef();
  t.current = e;
  var n = L.useCallback(function() {
    for (var r, o = arguments.length, s = new Array(o), i = 0; i < o; i++)
      s[i] = arguments[i];
    return (r = t.current) === null || r === void 0 ? void 0 : r.call.apply(r, [t].concat(s));
  }, []);
  return n;
}
function si(e) {
  if (Array.isArray(e)) return e;
}
function ii(e, t) {
  var n = e == null ? null : typeof Symbol < "u" && e[Symbol.iterator] || e["@@iterator"];
  if (n != null) {
    var r, o, s, i, a = [], l = !0, u = !1;
    try {
      if (s = (n = n.call(e)).next, t === 0) {
        if (Object(n) !== n) return;
        l = !1;
      } else for (; !(l = (r = s.call(n)).done) && (a.push(r.value), a.length !== t); l = !0) ;
    } catch (f) {
      u = !0, o = f;
    } finally {
      try {
        if (!l && n.return != null && (i = n.return(), Object(i) !== i)) return;
      } finally {
        if (u) throw o;
      }
    }
    return a;
  }
}
function Qn(e, t) {
  (t == null || t > e.length) && (t = e.length);
  for (var n = 0, r = Array(t); n < t; n++) r[n] = e[n];
  return r;
}
function ai(e, t) {
  if (e) {
    if (typeof e == "string") return Qn(e, t);
    var n = {}.toString.call(e).slice(8, -1);
    return n === "Object" && e.constructor && (n = e.constructor.name), n === "Map" || n === "Set" ? Array.from(e) : n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n) ? Qn(e, t) : void 0;
  }
}
function li() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function ne(e, t) {
  return si(e) || ii(e, t) || ai(e, t) || li();
}
function Et() {
  return !!(typeof window < "u" && window.document && window.document.createElement);
}
var Zn = Et() ? L.useLayoutEffect : L.useEffect, Br = function(t, n) {
  var r = L.useRef(!0);
  Zn(function() {
    return t(r.current);
  }, n), Zn(function() {
    return r.current = !1, function() {
      r.current = !0;
    };
  }, []);
}, Jn = function(t, n) {
  Br(function(r) {
    if (!r)
      return t();
  }, n);
};
function Je(e) {
  var t = L.useRef(!1), n = L.useState(e), r = ne(n, 2), o = r[0], s = r[1];
  L.useEffect(function() {
    return t.current = !1, function() {
      t.current = !0;
    };
  }, []);
  function i(a, l) {
    l && t.current || s(a);
  }
  return [o, i];
}
function Ut(e) {
  return e !== void 0;
}
function ci(e, t) {
  var n = t || {}, r = n.defaultValue, o = n.value, s = n.onChange, i = n.postState, a = Je(function() {
    return Ut(o) ? o : Ut(r) ? typeof r == "function" ? r() : r : typeof e == "function" ? e() : e;
  }), l = ne(a, 2), u = l[0], f = l[1], m = o !== void 0 ? o : u, d = i ? i(m) : m, h = Re(s), v = Je([m]), g = ne(v, 2), p = g[0], y = g[1];
  Jn(function() {
    var R = p[0];
    u !== R && h(u, R);
  }, [p]), Jn(function() {
    Ut(o) || f(o);
  }, [o]);
  var T = Re(function(R, $) {
    f(R, $), y([m], $);
  });
  return [d, T];
}
function ee(e) {
  "@babel/helpers - typeof";
  return ee = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, ee(e);
}
var Wr = {
  exports: {}
}, H = {};
/**
 * @license React
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Sn = Symbol.for("react.element"), xn = Symbol.for("react.portal"), Ct = Symbol.for("react.fragment"), Tt = Symbol.for("react.strict_mode"), $t = Symbol.for("react.profiler"), Rt = Symbol.for("react.provider"), Pt = Symbol.for("react.context"), ui = Symbol.for("react.server_context"), It = Symbol.for("react.forward_ref"), Mt = Symbol.for("react.suspense"), Lt = Symbol.for("react.suspense_list"), Nt = Symbol.for("react.memo"), Ft = Symbol.for("react.lazy"), di = Symbol.for("react.offscreen"), Vr;
Vr = Symbol.for("react.module.reference");
function de(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case Sn:
        switch (e = e.type, e) {
          case Ct:
          case $t:
          case Tt:
          case Mt:
          case Lt:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case ui:
              case Pt:
              case It:
              case Ft:
              case Nt:
              case Rt:
                return e;
              default:
                return t;
            }
        }
      case xn:
        return t;
    }
  }
}
H.ContextConsumer = Pt;
H.ContextProvider = Rt;
H.Element = Sn;
H.ForwardRef = It;
H.Fragment = Ct;
H.Lazy = Ft;
H.Memo = Nt;
H.Portal = xn;
H.Profiler = $t;
H.StrictMode = Tt;
H.Suspense = Mt;
H.SuspenseList = Lt;
H.isAsyncMode = function() {
  return !1;
};
H.isConcurrentMode = function() {
  return !1;
};
H.isContextConsumer = function(e) {
  return de(e) === Pt;
};
H.isContextProvider = function(e) {
  return de(e) === Rt;
};
H.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === Sn;
};
H.isForwardRef = function(e) {
  return de(e) === It;
};
H.isFragment = function(e) {
  return de(e) === Ct;
};
H.isLazy = function(e) {
  return de(e) === Ft;
};
H.isMemo = function(e) {
  return de(e) === Nt;
};
H.isPortal = function(e) {
  return de(e) === xn;
};
H.isProfiler = function(e) {
  return de(e) === $t;
};
H.isStrictMode = function(e) {
  return de(e) === Tt;
};
H.isSuspense = function(e) {
  return de(e) === Mt;
};
H.isSuspenseList = function(e) {
  return de(e) === Lt;
};
H.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === Ct || e === $t || e === Tt || e === Mt || e === Lt || e === di || typeof e == "object" && e !== null && (e.$$typeof === Ft || e.$$typeof === Nt || e.$$typeof === Rt || e.$$typeof === Pt || e.$$typeof === It || e.$$typeof === Vr || e.getModuleId !== void 0);
};
H.typeOf = de;
Wr.exports = H;
var Gt = Wr.exports, fi = Symbol.for("react.element"), mi = Symbol.for("react.transitional.element"), pi = Symbol.for("react.fragment");
function gi(e) {
  return (
    // Base object type
    e && ee(e) === "object" && // React Element type
    (e.$$typeof === fi || e.$$typeof === mi) && // React Fragment type
    e.type === pi
  );
}
var hi = Number(Io.split(".")[0]), yi = function(t, n) {
  typeof t == "function" ? t(n) : ee(t) === "object" && t && "current" in t && (t.current = n);
}, vi = function(t) {
  var n, r;
  if (!t)
    return !1;
  if (Xr(t) && hi >= 19)
    return !0;
  var o = Gt.isMemo(t) ? t.type.type : t.type;
  return !(typeof o == "function" && !((n = o.prototype) !== null && n !== void 0 && n.render) && o.$$typeof !== Gt.ForwardRef || typeof t == "function" && !((r = t.prototype) !== null && r !== void 0 && r.render) && t.$$typeof !== Gt.ForwardRef);
};
function Xr(e) {
  return /* @__PURE__ */ Po(e) && !gi(e);
}
var bi = function(t) {
  if (t && Xr(t)) {
    var n = t;
    return n.props.propertyIsEnumerable("ref") ? n.props.ref : n.ref;
  }
  return null;
};
function Si(e, t) {
  if (ee(e) != "object" || !e) return e;
  var n = e[Symbol.toPrimitive];
  if (n !== void 0) {
    var r = n.call(e, t);
    if (ee(r) != "object") return r;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (t === "string" ? String : Number)(e);
}
function Ur(e) {
  var t = Si(e, "string");
  return ee(t) == "symbol" ? t : t + "";
}
function A(e, t, n) {
  return (t = Ur(t)) in e ? Object.defineProperty(e, t, {
    value: n,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : e[t] = n, e;
}
function er(e, t) {
  var n = Object.keys(e);
  if (Object.getOwnPropertySymbols) {
    var r = Object.getOwnPropertySymbols(e);
    t && (r = r.filter(function(o) {
      return Object.getOwnPropertyDescriptor(e, o).enumerable;
    })), n.push.apply(n, r);
  }
  return n;
}
function O(e) {
  for (var t = 1; t < arguments.length; t++) {
    var n = arguments[t] != null ? arguments[t] : {};
    t % 2 ? er(Object(n), !0).forEach(function(r) {
      A(e, r, n[r]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(n)) : er(Object(n)).forEach(function(r) {
      Object.defineProperty(e, r, Object.getOwnPropertyDescriptor(n, r));
    });
  }
  return e;
}
const rt = /* @__PURE__ */ c.createContext(null);
function tr(e) {
  const {
    getDropContainer: t,
    className: n,
    prefixCls: r,
    children: o
  } = e, {
    disabled: s
  } = c.useContext(rt), [i, a] = c.useState(), [l, u] = c.useState(null);
  if (c.useEffect(() => {
    const d = t == null ? void 0 : t();
    i !== d && a(d);
  }, [t]), c.useEffect(() => {
    if (i) {
      const d = () => {
        u(!0);
      }, h = (p) => {
        p.preventDefault();
      }, v = (p) => {
        p.relatedTarget || u(!1);
      }, g = (p) => {
        u(!1), p.preventDefault();
      };
      return document.addEventListener("dragenter", d), document.addEventListener("dragover", h), document.addEventListener("dragleave", v), document.addEventListener("drop", g), () => {
        document.removeEventListener("dragenter", d), document.removeEventListener("dragover", h), document.removeEventListener("dragleave", v), document.removeEventListener("drop", g);
      };
    }
  }, [!!i]), !(t && i && !s))
    return null;
  const m = `${r}-drop-area`;
  return /* @__PURE__ */ ht(/* @__PURE__ */ c.createElement("div", {
    className: j(m, n, {
      [`${m}-on-body`]: i.tagName === "BODY"
    }),
    style: {
      display: l ? "block" : "none"
    }
  }, o), i);
}
function nr(e) {
  return e instanceof HTMLElement || e instanceof SVGElement;
}
function xi(e) {
  return e && ee(e) === "object" && nr(e.nativeElement) ? e.nativeElement : nr(e) ? e : null;
}
function wi(e) {
  var t = xi(e);
  if (t)
    return t;
  if (e instanceof c.Component) {
    var n;
    return (n = kn.findDOMNode) === null || n === void 0 ? void 0 : n.call(kn, e);
  }
  return null;
}
function _i(e, t) {
  if (e == null) return {};
  var n = {};
  for (var r in e) if ({}.hasOwnProperty.call(e, r)) {
    if (t.indexOf(r) !== -1) continue;
    n[r] = e[r];
  }
  return n;
}
function rr(e, t) {
  if (e == null) return {};
  var n, r, o = _i(e, t);
  if (Object.getOwnPropertySymbols) {
    var s = Object.getOwnPropertySymbols(e);
    for (r = 0; r < s.length; r++) n = s[r], t.indexOf(n) === -1 && {}.propertyIsEnumerable.call(e, n) && (o[n] = e[n]);
  }
  return o;
}
var Ei = /* @__PURE__ */ L.createContext({});
function Ge(e, t) {
  if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function");
}
function or(e, t) {
  for (var n = 0; n < t.length; n++) {
    var r = t[n];
    r.enumerable = r.enumerable || !1, r.configurable = !0, "value" in r && (r.writable = !0), Object.defineProperty(e, Ur(r.key), r);
  }
}
function qe(e, t, n) {
  return t && or(e.prototype, t), n && or(e, n), Object.defineProperty(e, "prototype", {
    writable: !1
  }), e;
}
function nn(e, t) {
  return nn = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(n, r) {
    return n.__proto__ = r, n;
  }, nn(e, t);
}
function Ot(e, t) {
  if (typeof t != "function" && t !== null) throw new TypeError("Super expression must either be null or a function");
  e.prototype = Object.create(t && t.prototype, {
    constructor: {
      value: e,
      writable: !0,
      configurable: !0
    }
  }), Object.defineProperty(e, "prototype", {
    writable: !1
  }), t && nn(e, t);
}
function vt(e) {
  return vt = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function(t) {
    return t.__proto__ || Object.getPrototypeOf(t);
  }, vt(e);
}
function Gr() {
  try {
    var e = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {
    }));
  } catch {
  }
  return (Gr = function() {
    return !!e;
  })();
}
function Le(e) {
  if (e === void 0) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return e;
}
function Ci(e, t) {
  if (t && (ee(t) == "object" || typeof t == "function")) return t;
  if (t !== void 0) throw new TypeError("Derived constructors may only return object or undefined");
  return Le(e);
}
function jt(e) {
  var t = Gr();
  return function() {
    var n, r = vt(e);
    if (t) {
      var o = vt(this).constructor;
      n = Reflect.construct(r, arguments, o);
    } else n = r.apply(this, arguments);
    return Ci(this, n);
  };
}
var Ti = /* @__PURE__ */ function(e) {
  Ot(n, e);
  var t = jt(n);
  function n() {
    return Ge(this, n), t.apply(this, arguments);
  }
  return qe(n, [{
    key: "render",
    value: function() {
      return this.props.children;
    }
  }]), n;
}(L.Component);
function $i(e) {
  var t = L.useReducer(function(a) {
    return a + 1;
  }, 0), n = ne(t, 2), r = n[1], o = L.useRef(e), s = Re(function() {
    return o.current;
  }), i = Re(function(a) {
    o.current = typeof a == "function" ? a(o.current) : a, r();
  });
  return [s, i];
}
var Ce = "none", st = "appear", it = "enter", at = "leave", sr = "none", pe = "prepare", He = "start", Be = "active", wn = "end", qr = "prepared";
function ir(e, t) {
  var n = {};
  return n[e.toLowerCase()] = t.toLowerCase(), n["Webkit".concat(e)] = "webkit".concat(t), n["Moz".concat(e)] = "moz".concat(t), n["ms".concat(e)] = "MS".concat(t), n["O".concat(e)] = "o".concat(t.toLowerCase()), n;
}
function Ri(e, t) {
  var n = {
    animationend: ir("Animation", "AnimationEnd"),
    transitionend: ir("Transition", "TransitionEnd")
  };
  return e && ("AnimationEvent" in t || delete n.animationend.animation, "TransitionEvent" in t || delete n.transitionend.transition), n;
}
var Pi = Ri(Et(), typeof window < "u" ? window : {}), Kr = {};
if (Et()) {
  var Ii = document.createElement("div");
  Kr = Ii.style;
}
var lt = {};
function Yr(e) {
  if (lt[e])
    return lt[e];
  var t = Pi[e];
  if (t)
    for (var n = Object.keys(t), r = n.length, o = 0; o < r; o += 1) {
      var s = n[o];
      if (Object.prototype.hasOwnProperty.call(t, s) && s in Kr)
        return lt[e] = t[s], lt[e];
    }
  return "";
}
var Qr = Yr("animationend"), Zr = Yr("transitionend"), Jr = !!(Qr && Zr), ar = Qr || "animationend", lr = Zr || "transitionend";
function cr(e, t) {
  if (!e) return null;
  if (ee(e) === "object") {
    var n = t.replace(/-\w/g, function(r) {
      return r[1].toUpperCase();
    });
    return e[n];
  }
  return "".concat(e, "-").concat(t);
}
const Mi = function(e) {
  var t = J();
  function n(o) {
    o && (o.removeEventListener(lr, e), o.removeEventListener(ar, e));
  }
  function r(o) {
    t.current && t.current !== o && n(t.current), o && o !== t.current && (o.addEventListener(lr, e), o.addEventListener(ar, e), t.current = o);
  }
  return L.useEffect(function() {
    return function() {
      n(t.current);
    };
  }, []), [r, n];
};
var eo = Et() ? Mo : _e, to = function(t) {
  return +setTimeout(t, 16);
}, no = function(t) {
  return clearTimeout(t);
};
typeof window < "u" && "requestAnimationFrame" in window && (to = function(t) {
  return window.requestAnimationFrame(t);
}, no = function(t) {
  return window.cancelAnimationFrame(t);
});
var ur = 0, _n = /* @__PURE__ */ new Map();
function ro(e) {
  _n.delete(e);
}
var rn = function(t) {
  var n = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 1;
  ur += 1;
  var r = ur;
  function o(s) {
    if (s === 0)
      ro(r), t();
    else {
      var i = to(function() {
        o(s - 1);
      });
      _n.set(r, i);
    }
  }
  return o(n), r;
};
rn.cancel = function(e) {
  var t = _n.get(e);
  return ro(e), no(t);
};
const Li = function() {
  var e = L.useRef(null);
  function t() {
    rn.cancel(e.current);
  }
  function n(r) {
    var o = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 2;
    t();
    var s = rn(function() {
      o <= 1 ? r({
        isCanceled: function() {
          return s !== e.current;
        }
      }) : n(r, o - 1);
    });
    e.current = s;
  }
  return L.useEffect(function() {
    return function() {
      t();
    };
  }, []), [n, t];
};
var Ni = [pe, He, Be, wn], Fi = [pe, qr], oo = !1, Oi = !0;
function so(e) {
  return e === Be || e === wn;
}
const ji = function(e, t, n) {
  var r = Je(sr), o = ne(r, 2), s = o[0], i = o[1], a = Li(), l = ne(a, 2), u = l[0], f = l[1];
  function m() {
    i(pe, !0);
  }
  var d = t ? Fi : Ni;
  return eo(function() {
    if (s !== sr && s !== wn) {
      var h = d.indexOf(s), v = d[h + 1], g = n(s);
      g === oo ? i(v, !0) : v && u(function(p) {
        function y() {
          p.isCanceled() || i(v, !0);
        }
        g === !0 ? y() : Promise.resolve(g).then(y);
      });
    }
  }, [e, s]), L.useEffect(function() {
    return function() {
      f();
    };
  }, []), [m, s];
};
function ki(e, t, n, r) {
  var o = r.motionEnter, s = o === void 0 ? !0 : o, i = r.motionAppear, a = i === void 0 ? !0 : i, l = r.motionLeave, u = l === void 0 ? !0 : l, f = r.motionDeadline, m = r.motionLeaveImmediately, d = r.onAppearPrepare, h = r.onEnterPrepare, v = r.onLeavePrepare, g = r.onAppearStart, p = r.onEnterStart, y = r.onLeaveStart, T = r.onAppearActive, R = r.onEnterActive, $ = r.onLeaveActive, E = r.onAppearEnd, x = r.onEnterEnd, I = r.onLeaveEnd, _ = r.onVisibleChanged, P = Je(), N = ne(P, 2), z = N[0], k = N[1], w = $i(Ce), b = ne(w, 2), M = b[0], F = b[1], D = Je(null), W = ne(D, 2), re = W[0], te = W[1], U = M(), B = J(!1), G = J(null);
  function V() {
    return n();
  }
  var q = J(!1);
  function Se() {
    F(Ce), te(null, !0);
  }
  var fe = Re(function(Z) {
    var Y = M();
    if (Y !== Ce) {
      var ie = V();
      if (!(Z && !Z.deadline && Z.target !== ie)) {
        var Pe = q.current, Ie;
        Y === st && Pe ? Ie = E == null ? void 0 : E(ie, Z) : Y === it && Pe ? Ie = x == null ? void 0 : x(ie, Z) : Y === at && Pe && (Ie = I == null ? void 0 : I(ie, Z)), Pe && Ie !== !1 && Se();
      }
    }
  }), Ye = Mi(fe), Oe = ne(Ye, 1), je = Oe[0], ke = function(Y) {
    switch (Y) {
      case st:
        return A(A(A({}, pe, d), He, g), Be, T);
      case it:
        return A(A(A({}, pe, h), He, p), Be, R);
      case at:
        return A(A(A({}, pe, v), He, y), Be, $);
      default:
        return {};
    }
  }, xe = L.useMemo(function() {
    return ke(U);
  }, [U]), Ae = ji(U, !e, function(Z) {
    if (Z === pe) {
      var Y = xe[pe];
      return Y ? Y(V()) : oo;
    }
    if (C in xe) {
      var ie;
      te(((ie = xe[C]) === null || ie === void 0 ? void 0 : ie.call(xe, V(), null)) || null);
    }
    return C === Be && U !== Ce && (je(V()), f > 0 && (clearTimeout(G.current), G.current = setTimeout(function() {
      fe({
        deadline: !0
      });
    }, f))), C === qr && Se(), Oi;
  }), ot = ne(Ae, 2), Bt = ot[0], C = ot[1], K = so(C);
  q.current = K;
  var X = J(null);
  eo(function() {
    if (!(B.current && X.current === t)) {
      k(t);
      var Z = B.current;
      B.current = !0;
      var Y;
      !Z && t && a && (Y = st), Z && t && s && (Y = it), (Z && !t && u || !Z && m && !t && u) && (Y = at);
      var ie = ke(Y);
      Y && (e || ie[pe]) ? (F(Y), Bt()) : F(Ce), X.current = t;
    }
  }, [t]), _e(function() {
    // Cancel appear
    (U === st && !a || // Cancel enter
    U === it && !s || // Cancel leave
    U === at && !u) && F(Ce);
  }, [a, s, u]), _e(function() {
    return function() {
      B.current = !1, clearTimeout(G.current);
    };
  }, []);
  var me = L.useRef(!1);
  _e(function() {
    z && (me.current = !0), z !== void 0 && U === Ce && ((me.current || z) && (_ == null || _(z)), me.current = !0);
  }, [z, U]);
  var ce = re;
  return xe[pe] && C === He && (ce = O({
    transition: "none"
  }, ce)), [U, C, ce, z ?? t];
}
function Ai(e) {
  var t = e;
  ee(e) === "object" && (t = e.transitionSupport);
  function n(o, s) {
    return !!(o.motionName && t && s !== !1);
  }
  var r = /* @__PURE__ */ L.forwardRef(function(o, s) {
    var i = o.visible, a = i === void 0 ? !0 : i, l = o.removeOnLeave, u = l === void 0 ? !0 : l, f = o.forceRender, m = o.children, d = o.motionName, h = o.leavedClassName, v = o.eventProps, g = L.useContext(Ei), p = g.motion, y = n(o, p), T = J(), R = J();
    function $() {
      try {
        return T.current instanceof HTMLElement ? T.current : wi(R.current);
      } catch {
        return null;
      }
    }
    var E = ki(y, a, $, o), x = ne(E, 4), I = x[0], _ = x[1], P = x[2], N = x[3], z = L.useRef(N);
    N && (z.current = !0);
    var k = L.useCallback(function(W) {
      T.current = W, yi(s, W);
    }, [s]), w, b = O(O({}, v), {}, {
      visible: a
    });
    if (!m)
      w = null;
    else if (I === Ce)
      N ? w = m(O({}, b), k) : !u && z.current && h ? w = m(O(O({}, b), {}, {
        className: h
      }), k) : f || !u && !h ? w = m(O(O({}, b), {}, {
        style: {
          display: "none"
        }
      }), k) : w = null;
    else {
      var M;
      _ === pe ? M = "prepare" : so(_) ? M = "active" : _ === He && (M = "start");
      var F = cr(d, "".concat(I, "-").concat(M));
      w = m(O(O({}, b), {}, {
        className: j(cr(d, I), A(A({}, F, F && M), d, typeof d == "string")),
        style: P
      }), k);
    }
    if (/* @__PURE__ */ L.isValidElement(w) && vi(w)) {
      var D = bi(w);
      D || (w = /* @__PURE__ */ L.cloneElement(w, {
        ref: k
      }));
    }
    return /* @__PURE__ */ L.createElement(Ti, {
      ref: R
    }, w);
  });
  return r.displayName = "CSSMotion", r;
}
const zi = Ai(Jr);
var on = "add", sn = "keep", an = "remove", qt = "removed";
function Di(e) {
  var t;
  return e && ee(e) === "object" && "key" in e ? t = e : t = {
    key: e
  }, O(O({}, t), {}, {
    key: String(t.key)
  });
}
function ln() {
  var e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [];
  return e.map(Di);
}
function Hi() {
  var e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [], t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : [], n = [], r = 0, o = t.length, s = ln(e), i = ln(t);
  s.forEach(function(u) {
    for (var f = !1, m = r; m < o; m += 1) {
      var d = i[m];
      if (d.key === u.key) {
        r < m && (n = n.concat(i.slice(r, m).map(function(h) {
          return O(O({}, h), {}, {
            status: on
          });
        })), r = m), n.push(O(O({}, d), {}, {
          status: sn
        })), r += 1, f = !0;
        break;
      }
    }
    f || n.push(O(O({}, u), {}, {
      status: an
    }));
  }), r < o && (n = n.concat(i.slice(r).map(function(u) {
    return O(O({}, u), {}, {
      status: on
    });
  })));
  var a = {};
  n.forEach(function(u) {
    var f = u.key;
    a[f] = (a[f] || 0) + 1;
  });
  var l = Object.keys(a).filter(function(u) {
    return a[u] > 1;
  });
  return l.forEach(function(u) {
    n = n.filter(function(f) {
      var m = f.key, d = f.status;
      return m !== u || d !== an;
    }), n.forEach(function(f) {
      f.key === u && (f.status = sn);
    });
  }), n;
}
var Bi = ["component", "children", "onVisibleChanged", "onAllRemoved"], Wi = ["status"], Vi = ["eventProps", "visible", "children", "motionName", "motionAppear", "motionEnter", "motionLeave", "motionLeaveImmediately", "motionDeadline", "removeOnLeave", "leavedClassName", "onAppearPrepare", "onAppearStart", "onAppearActive", "onAppearEnd", "onEnterStart", "onEnterActive", "onEnterEnd", "onLeaveStart", "onLeaveActive", "onLeaveEnd"];
function Xi(e) {
  var t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : zi, n = /* @__PURE__ */ function(r) {
    Ot(s, r);
    var o = jt(s);
    function s() {
      var i;
      Ge(this, s);
      for (var a = arguments.length, l = new Array(a), u = 0; u < a; u++)
        l[u] = arguments[u];
      return i = o.call.apply(o, [this].concat(l)), A(Le(i), "state", {
        keyEntities: []
      }), A(Le(i), "removeKey", function(f) {
        i.setState(function(m) {
          var d = m.keyEntities.map(function(h) {
            return h.key !== f ? h : O(O({}, h), {}, {
              status: qt
            });
          });
          return {
            keyEntities: d
          };
        }, function() {
          var m = i.state.keyEntities, d = m.filter(function(h) {
            var v = h.status;
            return v !== qt;
          }).length;
          d === 0 && i.props.onAllRemoved && i.props.onAllRemoved();
        });
      }), i;
    }
    return qe(s, [{
      key: "render",
      value: function() {
        var a = this, l = this.state.keyEntities, u = this.props, f = u.component, m = u.children, d = u.onVisibleChanged;
        u.onAllRemoved;
        var h = rr(u, Bi), v = f || L.Fragment, g = {};
        return Vi.forEach(function(p) {
          g[p] = h[p], delete h[p];
        }), delete h.keys, /* @__PURE__ */ L.createElement(v, h, l.map(function(p, y) {
          var T = p.status, R = rr(p, Wi), $ = T === on || T === sn;
          return /* @__PURE__ */ L.createElement(t, be({}, g, {
            key: R.key,
            visible: $,
            eventProps: R,
            onVisibleChanged: function(x) {
              d == null || d(x, {
                key: R.key
              }), x || a.removeKey(R.key);
            }
          }), function(E, x) {
            return m(O(O({}, E), {}, {
              index: y
            }), x);
          });
        }));
      }
    }], [{
      key: "getDerivedStateFromProps",
      value: function(a, l) {
        var u = a.keys, f = l.keyEntities, m = ln(u), d = Hi(f, m);
        return {
          keyEntities: d.filter(function(h) {
            var v = f.find(function(g) {
              var p = g.key;
              return h.key === p;
            });
            return !(v && v.status === qt && h.status === an);
          })
        };
      }
    }]), s;
  }(L.Component);
  return A(n, "defaultProps", {
    component: "div"
  }), n;
}
const Ui = Xi(Jr);
function Gi(e, t) {
  const {
    children: n,
    upload: r,
    rootClassName: o
  } = e, s = c.useRef(null);
  return c.useImperativeHandle(t, () => s.current), /* @__PURE__ */ c.createElement(Nr, be({}, r, {
    showUploadList: !1,
    rootClassName: o,
    ref: s
  }), n);
}
const io = /* @__PURE__ */ c.forwardRef(Gi);
var ao = /* @__PURE__ */ qe(function e() {
  Ge(this, e);
}), lo = "CALC_UNIT", qi = new RegExp(lo, "g");
function Kt(e) {
  return typeof e == "number" ? "".concat(e).concat(lo) : e;
}
var Ki = /* @__PURE__ */ function(e) {
  Ot(n, e);
  var t = jt(n);
  function n(r, o) {
    var s;
    Ge(this, n), s = t.call(this), A(Le(s), "result", ""), A(Le(s), "unitlessCssVar", void 0), A(Le(s), "lowPriority", void 0);
    var i = ee(r);
    return s.unitlessCssVar = o, r instanceof n ? s.result = "(".concat(r.result, ")") : i === "number" ? s.result = Kt(r) : i === "string" && (s.result = r), s;
  }
  return qe(n, [{
    key: "add",
    value: function(o) {
      return o instanceof n ? this.result = "".concat(this.result, " + ").concat(o.getResult()) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " + ").concat(Kt(o))), this.lowPriority = !0, this;
    }
  }, {
    key: "sub",
    value: function(o) {
      return o instanceof n ? this.result = "".concat(this.result, " - ").concat(o.getResult()) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " - ").concat(Kt(o))), this.lowPriority = !0, this;
    }
  }, {
    key: "mul",
    value: function(o) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), o instanceof n ? this.result = "".concat(this.result, " * ").concat(o.getResult(!0)) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " * ").concat(o)), this.lowPriority = !1, this;
    }
  }, {
    key: "div",
    value: function(o) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), o instanceof n ? this.result = "".concat(this.result, " / ").concat(o.getResult(!0)) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " / ").concat(o)), this.lowPriority = !1, this;
    }
  }, {
    key: "getResult",
    value: function(o) {
      return this.lowPriority || o ? "(".concat(this.result, ")") : this.result;
    }
  }, {
    key: "equal",
    value: function(o) {
      var s = this, i = o || {}, a = i.unit, l = !0;
      return typeof a == "boolean" ? l = a : Array.from(this.unitlessCssVar).some(function(u) {
        return s.result.includes(u);
      }) && (l = !1), this.result = this.result.replace(qi, l ? "px" : ""), typeof this.lowPriority < "u" ? "calc(".concat(this.result, ")") : this.result;
    }
  }]), n;
}(ao), Yi = /* @__PURE__ */ function(e) {
  Ot(n, e);
  var t = jt(n);
  function n(r) {
    var o;
    return Ge(this, n), o = t.call(this), A(Le(o), "result", 0), r instanceof n ? o.result = r.result : typeof r == "number" && (o.result = r), o;
  }
  return qe(n, [{
    key: "add",
    value: function(o) {
      return o instanceof n ? this.result += o.result : typeof o == "number" && (this.result += o), this;
    }
  }, {
    key: "sub",
    value: function(o) {
      return o instanceof n ? this.result -= o.result : typeof o == "number" && (this.result -= o), this;
    }
  }, {
    key: "mul",
    value: function(o) {
      return o instanceof n ? this.result *= o.result : typeof o == "number" && (this.result *= o), this;
    }
  }, {
    key: "div",
    value: function(o) {
      return o instanceof n ? this.result /= o.result : typeof o == "number" && (this.result /= o), this;
    }
  }, {
    key: "equal",
    value: function() {
      return this.result;
    }
  }]), n;
}(ao), Qi = function(t, n) {
  var r = t === "css" ? Ki : Yi;
  return function(o) {
    return new r(o, n);
  };
}, dr = function(t, n) {
  return "".concat([n, t.replace(/([A-Z]+)([A-Z][a-z]+)/g, "$1-$2").replace(/([a-z])([A-Z])/g, "$1-$2")].filter(Boolean).join("-"));
};
function fr(e, t, n, r) {
  var o = O({}, t[e]);
  if (r != null && r.deprecatedTokens) {
    var s = r.deprecatedTokens;
    s.forEach(function(a) {
      var l = ne(a, 2), u = l[0], f = l[1];
      if (o != null && o[u] || o != null && o[f]) {
        var m;
        (m = o[f]) !== null && m !== void 0 || (o[f] = o == null ? void 0 : o[u]);
      }
    });
  }
  var i = O(O({}, n), o);
  return Object.keys(i).forEach(function(a) {
    i[a] === t[a] && delete i[a];
  }), i;
}
var co = typeof CSSINJS_STATISTIC < "u", cn = !0;
function Ke() {
  for (var e = arguments.length, t = new Array(e), n = 0; n < e; n++)
    t[n] = arguments[n];
  if (!co)
    return Object.assign.apply(Object, [{}].concat(t));
  cn = !1;
  var r = {};
  return t.forEach(function(o) {
    if (ee(o) === "object") {
      var s = Object.keys(o);
      s.forEach(function(i) {
        Object.defineProperty(r, i, {
          configurable: !0,
          enumerable: !0,
          get: function() {
            return o[i];
          }
        });
      });
    }
  }), cn = !0, r;
}
var mr = {};
function Zi() {
}
var Ji = function(t) {
  var n, r = t, o = Zi;
  return co && typeof Proxy < "u" && (n = /* @__PURE__ */ new Set(), r = new Proxy(t, {
    get: function(i, a) {
      if (cn) {
        var l;
        (l = n) === null || l === void 0 || l.add(a);
      }
      return i[a];
    }
  }), o = function(i, a) {
    var l;
    mr[i] = {
      global: Array.from(n),
      component: O(O({}, (l = mr[i]) === null || l === void 0 ? void 0 : l.component), a)
    };
  }), {
    token: r,
    keys: n,
    flush: o
  };
};
function pr(e, t, n) {
  if (typeof n == "function") {
    var r;
    return n(Ke(t, (r = t[e]) !== null && r !== void 0 ? r : {}));
  }
  return n ?? {};
}
function ea(e) {
  return e === "js" ? {
    max: Math.max,
    min: Math.min
  } : {
    max: function() {
      for (var n = arguments.length, r = new Array(n), o = 0; o < n; o++)
        r[o] = arguments[o];
      return "max(".concat(r.map(function(s) {
        return Ve(s);
      }).join(","), ")");
    },
    min: function() {
      for (var n = arguments.length, r = new Array(n), o = 0; o < n; o++)
        r[o] = arguments[o];
      return "min(".concat(r.map(function(s) {
        return Ve(s);
      }).join(","), ")");
    }
  };
}
var ta = 1e3 * 60 * 10, na = /* @__PURE__ */ function() {
  function e() {
    Ge(this, e), A(this, "map", /* @__PURE__ */ new Map()), A(this, "objectIDMap", /* @__PURE__ */ new WeakMap()), A(this, "nextID", 0), A(this, "lastAccessBeat", /* @__PURE__ */ new Map()), A(this, "accessBeat", 0);
  }
  return qe(e, [{
    key: "set",
    value: function(n, r) {
      this.clear();
      var o = this.getCompositeKey(n);
      this.map.set(o, r), this.lastAccessBeat.set(o, Date.now());
    }
  }, {
    key: "get",
    value: function(n) {
      var r = this.getCompositeKey(n), o = this.map.get(r);
      return this.lastAccessBeat.set(r, Date.now()), this.accessBeat += 1, o;
    }
  }, {
    key: "getCompositeKey",
    value: function(n) {
      var r = this, o = n.map(function(s) {
        return s && ee(s) === "object" ? "obj_".concat(r.getObjectID(s)) : "".concat(ee(s), "_").concat(s);
      });
      return o.join("|");
    }
  }, {
    key: "getObjectID",
    value: function(n) {
      if (this.objectIDMap.has(n))
        return this.objectIDMap.get(n);
      var r = this.nextID;
      return this.objectIDMap.set(n, r), this.nextID += 1, r;
    }
  }, {
    key: "clear",
    value: function() {
      var n = this;
      if (this.accessBeat > 1e4) {
        var r = Date.now();
        this.lastAccessBeat.forEach(function(o, s) {
          r - o > ta && (n.map.delete(s), n.lastAccessBeat.delete(s));
        }), this.accessBeat = 0;
      }
    }
  }]), e;
}(), gr = new na();
function ra(e, t) {
  return c.useMemo(function() {
    var n = gr.get(t);
    if (n)
      return n;
    var r = e();
    return gr.set(t, r), r;
  }, t);
}
var oa = function() {
  return {};
};
function sa(e) {
  var t = e.useCSP, n = t === void 0 ? oa : t, r = e.useToken, o = e.usePrefix, s = e.getResetStyles, i = e.getCommonStyle, a = e.getCompUnitless;
  function l(d, h, v, g) {
    var p = Array.isArray(d) ? d[0] : d;
    function y(_) {
      return "".concat(String(p)).concat(_.slice(0, 1).toUpperCase()).concat(_.slice(1));
    }
    var T = (g == null ? void 0 : g.unitless) || {}, R = typeof a == "function" ? a(d) : {}, $ = O(O({}, R), {}, A({}, y("zIndexPopup"), !0));
    Object.keys(T).forEach(function(_) {
      $[y(_)] = T[_];
    });
    var E = O(O({}, g), {}, {
      unitless: $,
      prefixToken: y
    }), x = f(d, h, v, E), I = u(p, v, E);
    return function(_) {
      var P = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : _, N = x(_, P), z = ne(N, 2), k = z[1], w = I(P), b = ne(w, 2), M = b[0], F = b[1];
      return [M, k, F];
    };
  }
  function u(d, h, v) {
    var g = v.unitless, p = v.injectStyle, y = p === void 0 ? !0 : p, T = v.prefixToken, R = v.ignore, $ = function(I) {
      var _ = I.rootCls, P = I.cssVar, N = P === void 0 ? {} : P, z = r(), k = z.realToken;
      return ps({
        path: [d],
        prefix: N.prefix,
        key: N.key,
        unitless: g,
        ignore: R,
        token: k,
        scope: _
      }, function() {
        var w = pr(d, k, h), b = fr(d, k, w, {
          deprecatedTokens: v == null ? void 0 : v.deprecatedTokens
        });
        return Object.keys(w).forEach(function(M) {
          b[T(M)] = b[M], delete b[M];
        }), b;
      }), null;
    }, E = function(I) {
      var _ = r(), P = _.cssVar;
      return [function(N) {
        return y && P ? /* @__PURE__ */ c.createElement(c.Fragment, null, /* @__PURE__ */ c.createElement($, {
          rootCls: I,
          cssVar: P,
          component: d
        }), N) : N;
      }, P == null ? void 0 : P.key];
    };
    return E;
  }
  function f(d, h, v) {
    var g = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, p = Array.isArray(d) ? d : [d, d], y = ne(p, 1), T = y[0], R = p.join("-"), $ = e.layer || {
      name: "antd"
    };
    return function(E) {
      var x = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : E, I = r(), _ = I.theme, P = I.realToken, N = I.hashId, z = I.token, k = I.cssVar, w = o(), b = w.rootPrefixCls, M = w.iconPrefixCls, F = n(), D = k ? "css" : "js", W = ra(function() {
        var V = /* @__PURE__ */ new Set();
        return k && Object.keys(g.unitless || {}).forEach(function(q) {
          V.add(Wt(q, k.prefix)), V.add(Wt(q, dr(T, k.prefix)));
        }), Qi(D, V);
      }, [D, T, k == null ? void 0 : k.prefix]), re = ea(D), te = re.max, U = re.min, B = {
        theme: _,
        token: z,
        hashId: N,
        nonce: function() {
          return F.nonce;
        },
        clientOnly: g.clientOnly,
        layer: $,
        // antd is always at top of styles
        order: g.order || -999
      };
      typeof s == "function" && Dn(O(O({}, B), {}, {
        clientOnly: !1,
        path: ["Shared", b]
      }), function() {
        return s(z, {
          prefix: {
            rootPrefixCls: b,
            iconPrefixCls: M
          },
          csp: F
        });
      });
      var G = Dn(O(O({}, B), {}, {
        path: [R, E, M]
      }), function() {
        if (g.injectStyle === !1)
          return [];
        var V = Ji(z), q = V.token, Se = V.flush, fe = pr(T, P, v), Ye = ".".concat(E), Oe = fr(T, P, fe, {
          deprecatedTokens: g.deprecatedTokens
        });
        k && fe && ee(fe) === "object" && Object.keys(fe).forEach(function(Ae) {
          fe[Ae] = "var(".concat(Wt(Ae, dr(T, k.prefix)), ")");
        });
        var je = Ke(q, {
          componentCls: Ye,
          prefixCls: E,
          iconCls: ".".concat(M),
          antCls: ".".concat(b),
          calc: W,
          // @ts-ignore
          max: te,
          // @ts-ignore
          min: U
        }, k ? fe : Oe), ke = h(je, {
          hashId: N,
          prefixCls: E,
          rootPrefixCls: b,
          iconPrefixCls: M
        });
        Se(T, Oe);
        var xe = typeof i == "function" ? i(je, E, x, g.resetFont) : null;
        return [g.resetStyle === !1 ? null : xe, ke];
      });
      return [G, N];
    };
  }
  function m(d, h, v) {
    var g = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, p = f(d, h, v, O({
      resetStyle: !1,
      // Sub Style should default after root one
      order: -998
    }, g)), y = function(R) {
      var $ = R.prefixCls, E = R.rootCls, x = E === void 0 ? $ : E;
      return p($, x), null;
    };
    return y;
  }
  return {
    genStyleHooks: l,
    genSubStyleComponent: m,
    genComponentStyleHook: f
  };
}
const Q = Math.round;
function Yt(e, t) {
  const n = e.replace(/^[^(]*\((.*)/, "$1").replace(/\).*/, "").match(/\d*\.?\d+%?/g) || [], r = n.map((o) => parseFloat(o));
  for (let o = 0; o < 3; o += 1)
    r[o] = t(r[o] || 0, n[o] || "", o);
  return n[3] ? r[3] = n[3].includes("%") ? r[3] / 100 : r[3] : r[3] = 1, r;
}
const hr = (e, t, n) => n === 0 ? e : e / 100;
function Qe(e, t) {
  const n = t || 255;
  return e > n ? n : e < 0 ? 0 : e;
}
class ye {
  constructor(t) {
    A(this, "isValid", !0), A(this, "r", 0), A(this, "g", 0), A(this, "b", 0), A(this, "a", 1), A(this, "_h", void 0), A(this, "_s", void 0), A(this, "_l", void 0), A(this, "_v", void 0), A(this, "_max", void 0), A(this, "_min", void 0), A(this, "_brightness", void 0);
    function n(r) {
      return r[0] in t && r[1] in t && r[2] in t;
    }
    if (t) if (typeof t == "string") {
      let o = function(s) {
        return r.startsWith(s);
      };
      const r = t.trim();
      /^#?[A-F\d]{3,8}$/i.test(r) ? this.fromHexString(r) : o("rgb") ? this.fromRgbString(r) : o("hsl") ? this.fromHslString(r) : (o("hsv") || o("hsb")) && this.fromHsvString(r);
    } else if (t instanceof ye)
      this.r = t.r, this.g = t.g, this.b = t.b, this.a = t.a, this._h = t._h, this._s = t._s, this._l = t._l, this._v = t._v;
    else if (n("rgb"))
      this.r = Qe(t.r), this.g = Qe(t.g), this.b = Qe(t.b), this.a = typeof t.a == "number" ? Qe(t.a, 1) : 1;
    else if (n("hsl"))
      this.fromHsl(t);
    else if (n("hsv"))
      this.fromHsv(t);
    else
      throw new Error("@ant-design/fast-color: unsupported input " + JSON.stringify(t));
  }
  // ======================= Setter =======================
  setR(t) {
    return this._sc("r", t);
  }
  setG(t) {
    return this._sc("g", t);
  }
  setB(t) {
    return this._sc("b", t);
  }
  setA(t) {
    return this._sc("a", t, 1);
  }
  setHue(t) {
    const n = this.toHsv();
    return n.h = t, this._c(n);
  }
  // ======================= Getter =======================
  /**
   * Returns the perceived luminance of a color, from 0-1.
   * @see http://www.w3.org/TR/2008/REC-WCAG20-20081211/#relativeluminancedef
   */
  getLuminance() {
    function t(s) {
      const i = s / 255;
      return i <= 0.03928 ? i / 12.92 : Math.pow((i + 0.055) / 1.055, 2.4);
    }
    const n = t(this.r), r = t(this.g), o = t(this.b);
    return 0.2126 * n + 0.7152 * r + 0.0722 * o;
  }
  getHue() {
    if (typeof this._h > "u") {
      const t = this.getMax() - this.getMin();
      t === 0 ? this._h = 0 : this._h = Q(60 * (this.r === this.getMax() ? (this.g - this.b) / t + (this.g < this.b ? 6 : 0) : this.g === this.getMax() ? (this.b - this.r) / t + 2 : (this.r - this.g) / t + 4));
    }
    return this._h;
  }
  getSaturation() {
    if (typeof this._s > "u") {
      const t = this.getMax() - this.getMin();
      t === 0 ? this._s = 0 : this._s = t / this.getMax();
    }
    return this._s;
  }
  getLightness() {
    return typeof this._l > "u" && (this._l = (this.getMax() + this.getMin()) / 510), this._l;
  }
  getValue() {
    return typeof this._v > "u" && (this._v = this.getMax() / 255), this._v;
  }
  /**
   * Returns the perceived brightness of the color, from 0-255.
   * Note: this is not the b of HSB
   * @see http://www.w3.org/TR/AERT#color-contrast
   */
  getBrightness() {
    return typeof this._brightness > "u" && (this._brightness = (this.r * 299 + this.g * 587 + this.b * 114) / 1e3), this._brightness;
  }
  // ======================== Func ========================
  darken(t = 10) {
    const n = this.getHue(), r = this.getSaturation();
    let o = this.getLightness() - t / 100;
    return o < 0 && (o = 0), this._c({
      h: n,
      s: r,
      l: o,
      a: this.a
    });
  }
  lighten(t = 10) {
    const n = this.getHue(), r = this.getSaturation();
    let o = this.getLightness() + t / 100;
    return o > 1 && (o = 1), this._c({
      h: n,
      s: r,
      l: o,
      a: this.a
    });
  }
  /**
   * Mix the current color a given amount with another color, from 0 to 100.
   * 0 means no mixing (return current color).
   */
  mix(t, n = 50) {
    const r = this._c(t), o = n / 100, s = (a) => (r[a] - this[a]) * o + this[a], i = {
      r: Q(s("r")),
      g: Q(s("g")),
      b: Q(s("b")),
      a: Q(s("a") * 100) / 100
    };
    return this._c(i);
  }
  /**
   * Mix the color with pure white, from 0 to 100.
   * Providing 0 will do nothing, providing 100 will always return white.
   */
  tint(t = 10) {
    return this.mix({
      r: 255,
      g: 255,
      b: 255,
      a: 1
    }, t);
  }
  /**
   * Mix the color with pure black, from 0 to 100.
   * Providing 0 will do nothing, providing 100 will always return black.
   */
  shade(t = 10) {
    return this.mix({
      r: 0,
      g: 0,
      b: 0,
      a: 1
    }, t);
  }
  onBackground(t) {
    const n = this._c(t), r = this.a + n.a * (1 - this.a), o = (s) => Q((this[s] * this.a + n[s] * n.a * (1 - this.a)) / r);
    return this._c({
      r: o("r"),
      g: o("g"),
      b: o("b"),
      a: r
    });
  }
  // ======================= Status =======================
  isDark() {
    return this.getBrightness() < 128;
  }
  isLight() {
    return this.getBrightness() >= 128;
  }
  // ======================== MISC ========================
  equals(t) {
    return this.r === t.r && this.g === t.g && this.b === t.b && this.a === t.a;
  }
  clone() {
    return this._c(this);
  }
  // ======================= Format =======================
  toHexString() {
    let t = "#";
    const n = (this.r || 0).toString(16);
    t += n.length === 2 ? n : "0" + n;
    const r = (this.g || 0).toString(16);
    t += r.length === 2 ? r : "0" + r;
    const o = (this.b || 0).toString(16);
    if (t += o.length === 2 ? o : "0" + o, typeof this.a == "number" && this.a >= 0 && this.a < 1) {
      const s = Q(this.a * 255).toString(16);
      t += s.length === 2 ? s : "0" + s;
    }
    return t;
  }
  /** CSS support color pattern */
  toHsl() {
    return {
      h: this.getHue(),
      s: this.getSaturation(),
      l: this.getLightness(),
      a: this.a
    };
  }
  /** CSS support color pattern */
  toHslString() {
    const t = this.getHue(), n = Q(this.getSaturation() * 100), r = Q(this.getLightness() * 100);
    return this.a !== 1 ? `hsla(${t},${n}%,${r}%,${this.a})` : `hsl(${t},${n}%,${r}%)`;
  }
  /** Same as toHsb */
  toHsv() {
    return {
      h: this.getHue(),
      s: this.getSaturation(),
      v: this.getValue(),
      a: this.a
    };
  }
  toRgb() {
    return {
      r: this.r,
      g: this.g,
      b: this.b,
      a: this.a
    };
  }
  toRgbString() {
    return this.a !== 1 ? `rgba(${this.r},${this.g},${this.b},${this.a})` : `rgb(${this.r},${this.g},${this.b})`;
  }
  toString() {
    return this.toRgbString();
  }
  // ====================== Privates ======================
  /** Return a new FastColor object with one channel changed */
  _sc(t, n, r) {
    const o = this.clone();
    return o[t] = Qe(n, r), o;
  }
  _c(t) {
    return new this.constructor(t);
  }
  getMax() {
    return typeof this._max > "u" && (this._max = Math.max(this.r, this.g, this.b)), this._max;
  }
  getMin() {
    return typeof this._min > "u" && (this._min = Math.min(this.r, this.g, this.b)), this._min;
  }
  fromHexString(t) {
    const n = t.replace("#", "");
    function r(o, s) {
      return parseInt(n[o] + n[s || o], 16);
    }
    n.length < 6 ? (this.r = r(0), this.g = r(1), this.b = r(2), this.a = n[3] ? r(3) / 255 : 1) : (this.r = r(0, 1), this.g = r(2, 3), this.b = r(4, 5), this.a = n[6] ? r(6, 7) / 255 : 1);
  }
  fromHsl({
    h: t,
    s: n,
    l: r,
    a: o
  }) {
    if (this._h = t % 360, this._s = n, this._l = r, this.a = typeof o == "number" ? o : 1, n <= 0) {
      const d = Q(r * 255);
      this.r = d, this.g = d, this.b = d;
    }
    let s = 0, i = 0, a = 0;
    const l = t / 60, u = (1 - Math.abs(2 * r - 1)) * n, f = u * (1 - Math.abs(l % 2 - 1));
    l >= 0 && l < 1 ? (s = u, i = f) : l >= 1 && l < 2 ? (s = f, i = u) : l >= 2 && l < 3 ? (i = u, a = f) : l >= 3 && l < 4 ? (i = f, a = u) : l >= 4 && l < 5 ? (s = f, a = u) : l >= 5 && l < 6 && (s = u, a = f);
    const m = r - u / 2;
    this.r = Q((s + m) * 255), this.g = Q((i + m) * 255), this.b = Q((a + m) * 255);
  }
  fromHsv({
    h: t,
    s: n,
    v: r,
    a: o
  }) {
    this._h = t % 360, this._s = n, this._v = r, this.a = typeof o == "number" ? o : 1;
    const s = Q(r * 255);
    if (this.r = s, this.g = s, this.b = s, n <= 0)
      return;
    const i = t / 60, a = Math.floor(i), l = i - a, u = Q(r * (1 - n) * 255), f = Q(r * (1 - n * l) * 255), m = Q(r * (1 - n * (1 - l)) * 255);
    switch (a) {
      case 0:
        this.g = m, this.b = u;
        break;
      case 1:
        this.r = f, this.b = u;
        break;
      case 2:
        this.r = u, this.b = m;
        break;
      case 3:
        this.r = u, this.g = f;
        break;
      case 4:
        this.r = m, this.g = u;
        break;
      case 5:
      default:
        this.g = u, this.b = f;
        break;
    }
  }
  fromHsvString(t) {
    const n = Yt(t, hr);
    this.fromHsv({
      h: n[0],
      s: n[1],
      v: n[2],
      a: n[3]
    });
  }
  fromHslString(t) {
    const n = Yt(t, hr);
    this.fromHsl({
      h: n[0],
      s: n[1],
      l: n[2],
      a: n[3]
    });
  }
  fromRgbString(t) {
    const n = Yt(t, (r, o) => (
      // Convert percentage to number. e.g. 50% -> 128
      o.includes("%") ? Q(r / 100 * 255) : r
    ));
    this.r = n[0], this.g = n[1], this.b = n[2], this.a = n[3];
  }
}
const ia = {
  blue: "#1677FF",
  purple: "#722ED1",
  cyan: "#13C2C2",
  green: "#52C41A",
  magenta: "#EB2F96",
  /**
   * @deprecated Use magenta instead
   */
  pink: "#EB2F96",
  red: "#F5222D",
  orange: "#FA8C16",
  yellow: "#FADB14",
  volcano: "#FA541C",
  geekblue: "#2F54EB",
  gold: "#FAAD14",
  lime: "#A0D911"
}, aa = Object.assign(Object.assign({}, ia), {
  // Color
  colorPrimary: "#1677ff",
  colorSuccess: "#52c41a",
  colorWarning: "#faad14",
  colorError: "#ff4d4f",
  colorInfo: "#1677ff",
  colorLink: "",
  colorTextBase: "",
  colorBgBase: "",
  // Font
  fontFamily: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol',
'Noto Color Emoji'`,
  fontFamilyCode: "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace",
  fontSize: 14,
  // Line
  lineWidth: 1,
  lineType: "solid",
  // Motion
  motionUnit: 0.1,
  motionBase: 0,
  motionEaseOutCirc: "cubic-bezier(0.08, 0.82, 0.17, 1)",
  motionEaseInOutCirc: "cubic-bezier(0.78, 0.14, 0.15, 0.86)",
  motionEaseOut: "cubic-bezier(0.215, 0.61, 0.355, 1)",
  motionEaseInOut: "cubic-bezier(0.645, 0.045, 0.355, 1)",
  motionEaseOutBack: "cubic-bezier(0.12, 0.4, 0.29, 1.46)",
  motionEaseInBack: "cubic-bezier(0.71, -0.46, 0.88, 0.6)",
  motionEaseInQuint: "cubic-bezier(0.755, 0.05, 0.855, 0.06)",
  motionEaseOutQuint: "cubic-bezier(0.23, 1, 0.32, 1)",
  // Radius
  borderRadius: 6,
  // Size
  sizeUnit: 4,
  sizeStep: 4,
  sizePopupArrow: 16,
  // Control Base
  controlHeight: 32,
  // zIndex
  zIndexBase: 0,
  zIndexPopupBase: 1e3,
  // Image
  opacityImage: 1,
  // Wireframe
  wireframe: !1,
  // Motion
  motion: !0
});
function Qt(e) {
  return e >= 0 && e <= 255;
}
function ct(e, t) {
  const {
    r: n,
    g: r,
    b: o,
    a: s
  } = new ye(e).toRgb();
  if (s < 1)
    return e;
  const {
    r: i,
    g: a,
    b: l
  } = new ye(t).toRgb();
  for (let u = 0.01; u <= 1; u += 0.01) {
    const f = Math.round((n - i * (1 - u)) / u), m = Math.round((r - a * (1 - u)) / u), d = Math.round((o - l * (1 - u)) / u);
    if (Qt(f) && Qt(m) && Qt(d))
      return new ye({
        r: f,
        g: m,
        b: d,
        a: Math.round(u * 100) / 100
      }).toRgbString();
  }
  return new ye({
    r: n,
    g: r,
    b: o,
    a: 1
  }).toRgbString();
}
var la = function(e, t) {
  var n = {};
  for (var r in e) Object.prototype.hasOwnProperty.call(e, r) && t.indexOf(r) < 0 && (n[r] = e[r]);
  if (e != null && typeof Object.getOwnPropertySymbols == "function") for (var o = 0, r = Object.getOwnPropertySymbols(e); o < r.length; o++)
    t.indexOf(r[o]) < 0 && Object.prototype.propertyIsEnumerable.call(e, r[o]) && (n[r[o]] = e[r[o]]);
  return n;
};
function ca(e) {
  const {
    override: t
  } = e, n = la(e, ["override"]), r = Object.assign({}, t);
  Object.keys(aa).forEach((d) => {
    delete r[d];
  });
  const o = Object.assign(Object.assign({}, n), r), s = 480, i = 576, a = 768, l = 992, u = 1200, f = 1600;
  if (o.motion === !1) {
    const d = "0s";
    o.motionDurationFast = d, o.motionDurationMid = d, o.motionDurationSlow = d;
  }
  return Object.assign(Object.assign(Object.assign({}, o), {
    // ============== Background ============== //
    colorFillContent: o.colorFillSecondary,
    colorFillContentHover: o.colorFill,
    colorFillAlter: o.colorFillQuaternary,
    colorBgContainerDisabled: o.colorFillTertiary,
    // ============== Split ============== //
    colorBorderBg: o.colorBgContainer,
    colorSplit: ct(o.colorBorderSecondary, o.colorBgContainer),
    // ============== Text ============== //
    colorTextPlaceholder: o.colorTextQuaternary,
    colorTextDisabled: o.colorTextQuaternary,
    colorTextHeading: o.colorText,
    colorTextLabel: o.colorTextSecondary,
    colorTextDescription: o.colorTextTertiary,
    colorTextLightSolid: o.colorWhite,
    colorHighlight: o.colorError,
    colorBgTextHover: o.colorFillSecondary,
    colorBgTextActive: o.colorFill,
    colorIcon: o.colorTextTertiary,
    colorIconHover: o.colorText,
    colorErrorOutline: ct(o.colorErrorBg, o.colorBgContainer),
    colorWarningOutline: ct(o.colorWarningBg, o.colorBgContainer),
    // Font
    fontSizeIcon: o.fontSizeSM,
    // Line
    lineWidthFocus: o.lineWidth * 3,
    // Control
    lineWidth: o.lineWidth,
    controlOutlineWidth: o.lineWidth * 2,
    // Checkbox size and expand icon size
    controlInteractiveSize: o.controlHeight / 2,
    controlItemBgHover: o.colorFillTertiary,
    controlItemBgActive: o.colorPrimaryBg,
    controlItemBgActiveHover: o.colorPrimaryBgHover,
    controlItemBgActiveDisabled: o.colorFill,
    controlTmpOutline: o.colorFillQuaternary,
    controlOutline: ct(o.colorPrimaryBg, o.colorBgContainer),
    lineType: o.lineType,
    borderRadius: o.borderRadius,
    borderRadiusXS: o.borderRadiusXS,
    borderRadiusSM: o.borderRadiusSM,
    borderRadiusLG: o.borderRadiusLG,
    fontWeightStrong: 600,
    opacityLoading: 0.65,
    linkDecoration: "none",
    linkHoverDecoration: "none",
    linkFocusDecoration: "none",
    controlPaddingHorizontal: 12,
    controlPaddingHorizontalSM: 8,
    paddingXXS: o.sizeXXS,
    paddingXS: o.sizeXS,
    paddingSM: o.sizeSM,
    padding: o.size,
    paddingMD: o.sizeMD,
    paddingLG: o.sizeLG,
    paddingXL: o.sizeXL,
    paddingContentHorizontalLG: o.sizeLG,
    paddingContentVerticalLG: o.sizeMS,
    paddingContentHorizontal: o.sizeMS,
    paddingContentVertical: o.sizeSM,
    paddingContentHorizontalSM: o.size,
    paddingContentVerticalSM: o.sizeXS,
    marginXXS: o.sizeXXS,
    marginXS: o.sizeXS,
    marginSM: o.sizeSM,
    margin: o.size,
    marginMD: o.sizeMD,
    marginLG: o.sizeLG,
    marginXL: o.sizeXL,
    marginXXL: o.sizeXXL,
    boxShadow: `
      0 6px 16px 0 rgba(0, 0, 0, 0.08),
      0 3px 6px -4px rgba(0, 0, 0, 0.12),
      0 9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowSecondary: `
      0 6px 16px 0 rgba(0, 0, 0, 0.08),
      0 3px 6px -4px rgba(0, 0, 0, 0.12),
      0 9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowTertiary: `
      0 1px 2px 0 rgba(0, 0, 0, 0.03),
      0 1px 6px -1px rgba(0, 0, 0, 0.02),
      0 2px 4px 0 rgba(0, 0, 0, 0.02)
    `,
    screenXS: s,
    screenXSMin: s,
    screenXSMax: i - 1,
    screenSM: i,
    screenSMMin: i,
    screenSMMax: a - 1,
    screenMD: a,
    screenMDMin: a,
    screenMDMax: l - 1,
    screenLG: l,
    screenLGMin: l,
    screenLGMax: u - 1,
    screenXL: u,
    screenXLMin: u,
    screenXLMax: f - 1,
    screenXXL: f,
    screenXXLMin: f,
    boxShadowPopoverArrow: "2px 2px 5px rgba(0, 0, 0, 0.05)",
    boxShadowCard: `
      0 1px 2px -2px ${new ye("rgba(0, 0, 0, 0.16)").toRgbString()},
      0 3px 6px 0 ${new ye("rgba(0, 0, 0, 0.12)").toRgbString()},
      0 5px 12px 4px ${new ye("rgba(0, 0, 0, 0.09)").toRgbString()}
    `,
    boxShadowDrawerRight: `
      -6px 0 16px 0 rgba(0, 0, 0, 0.08),
      -3px 0 6px -4px rgba(0, 0, 0, 0.12),
      -9px 0 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowDrawerLeft: `
      6px 0 16px 0 rgba(0, 0, 0, 0.08),
      3px 0 6px -4px rgba(0, 0, 0, 0.12),
      9px 0 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowDrawerUp: `
      0 6px 16px 0 rgba(0, 0, 0, 0.08),
      0 3px 6px -4px rgba(0, 0, 0, 0.12),
      0 9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowDrawerDown: `
      0 -6px 16px 0 rgba(0, 0, 0, 0.08),
      0 -3px 6px -4px rgba(0, 0, 0, 0.12),
      0 -9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowTabsOverflowLeft: "inset 10px 0 8px -8px rgba(0, 0, 0, 0.08)",
    boxShadowTabsOverflowRight: "inset -10px 0 8px -8px rgba(0, 0, 0, 0.08)",
    boxShadowTabsOverflowTop: "inset 0 10px 8px -8px rgba(0, 0, 0, 0.08)",
    boxShadowTabsOverflowBottom: "inset 0 -10px 8px -8px rgba(0, 0, 0, 0.08)"
  }), r);
}
const ua = {
  lineHeight: !0,
  lineHeightSM: !0,
  lineHeightLG: !0,
  lineHeightHeading1: !0,
  lineHeightHeading2: !0,
  lineHeightHeading3: !0,
  lineHeightHeading4: !0,
  lineHeightHeading5: !0,
  opacityLoading: !0,
  fontWeightStrong: !0,
  zIndexPopupBase: !0,
  zIndexBase: !0,
  opacityImage: !0
}, da = {
  size: !0,
  sizeSM: !0,
  sizeLG: !0,
  sizeMD: !0,
  sizeXS: !0,
  sizeXXS: !0,
  sizeMS: !0,
  sizeXL: !0,
  sizeXXL: !0,
  sizeUnit: !0,
  sizeStep: !0,
  motionBase: !0,
  motionUnit: !0
}, fa = gs(We.defaultAlgorithm), ma = {
  screenXS: !0,
  screenXSMin: !0,
  screenXSMax: !0,
  screenSM: !0,
  screenSMMin: !0,
  screenSMMax: !0,
  screenMD: !0,
  screenMDMin: !0,
  screenMDMax: !0,
  screenLG: !0,
  screenLGMin: !0,
  screenLGMax: !0,
  screenXL: !0,
  screenXLMin: !0,
  screenXLMax: !0,
  screenXXL: !0,
  screenXXLMin: !0
}, uo = (e, t, n) => {
  const r = n.getDerivativeToken(e), {
    override: o,
    ...s
  } = t;
  let i = {
    ...r,
    override: o
  };
  return i = ca(i), s && Object.entries(s).forEach(([a, l]) => {
    const {
      theme: u,
      ...f
    } = l;
    let m = f;
    u && (m = uo({
      ...i,
      ...f
    }, {
      override: f
    }, u)), i[a] = m;
  }), i;
};
function pa() {
  const {
    token: e,
    hashed: t,
    theme: n = fa,
    override: r,
    cssVar: o
  } = c.useContext(We._internalContext), [s, i, a] = hs(n, [We.defaultSeed, e], {
    salt: `${ni}-${t || ""}`,
    override: r,
    getComputedToken: uo,
    cssVar: o && {
      prefix: o.prefix,
      key: o.key,
      unitless: ua,
      ignore: da,
      preserve: ma
    }
  });
  return [n, a, t ? i : "", s, o];
}
const {
  genStyleHooks: kt
} = sa({
  usePrefix: () => {
    const {
      getPrefixCls: e,
      iconPrefixCls: t
    } = $e();
    return {
      iconPrefixCls: t,
      rootPrefixCls: e()
    };
  },
  useToken: () => {
    const [e, t, n, r, o] = pa();
    return {
      theme: e,
      realToken: t,
      hashId: n,
      token: r,
      cssVar: o
    };
  },
  useCSP: () => {
    const {
      csp: e
    } = $e();
    return e ?? {};
  },
  layer: {
    name: "antdx",
    dependencies: ["antd"]
  }
}), ga = (e) => {
  const {
    componentCls: t,
    calc: n
  } = e, r = `${t}-list-card`, o = n(e.fontSize).mul(e.lineHeight).mul(2).add(e.paddingSM).add(e.paddingSM).equal();
  return {
    [r]: {
      borderRadius: e.borderRadius,
      position: "relative",
      background: e.colorFillContent,
      borderWidth: e.lineWidth,
      borderStyle: "solid",
      borderColor: "transparent",
      flex: "none",
      // =============================== Desc ================================
      [`${r}-name,${r}-desc`]: {
        display: "flex",
        flexWrap: "nowrap",
        maxWidth: "100%"
      },
      [`${r}-ellipsis-prefix`]: {
        flex: "0 1 auto",
        minWidth: 0,
        overflow: "hidden",
        textOverflow: "ellipsis",
        whiteSpace: "nowrap"
      },
      [`${r}-ellipsis-suffix`]: {
        flex: "none"
      },
      // ============================= Overview ==============================
      "&-type-overview": {
        padding: n(e.paddingSM).sub(e.lineWidth).equal(),
        paddingInlineStart: n(e.padding).add(e.lineWidth).equal(),
        display: "flex",
        flexWrap: "nowrap",
        gap: e.paddingXS,
        alignItems: "flex-start",
        width: 236,
        // Icon
        [`${r}-icon`]: {
          fontSize: n(e.fontSizeLG).mul(2).equal(),
          lineHeight: 1,
          paddingTop: n(e.paddingXXS).mul(1.5).equal(),
          flex: "none"
        },
        // Content
        [`${r}-content`]: {
          flex: "auto",
          minWidth: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "stretch"
        },
        [`${r}-desc`]: {
          color: e.colorTextTertiary
        }
      },
      // ============================== Preview ==============================
      "&-type-preview": {
        width: o,
        height: o,
        lineHeight: 1,
        [`&:not(${r}-status-error)`]: {
          border: 0
        },
        // Img
        img: {
          width: "100%",
          height: "100%",
          verticalAlign: "top",
          objectFit: "cover",
          borderRadius: "inherit"
        },
        // Mask
        [`${r}-img-mask`]: {
          position: "absolute",
          inset: 0,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          background: `rgba(0, 0, 0, ${e.opacityLoading})`,
          borderRadius: "inherit"
        },
        // Error
        [`&${r}-status-error`]: {
          [`img, ${r}-img-mask`]: {
            borderRadius: n(e.borderRadius).sub(e.lineWidth).equal()
          },
          [`${r}-desc`]: {
            paddingInline: e.paddingXXS
          }
        },
        // Progress
        [`${r}-progress`]: {}
      },
      // ============================ Remove Icon ============================
      [`${r}-remove`]: {
        position: "absolute",
        top: 0,
        insetInlineEnd: 0,
        border: 0,
        padding: e.paddingXXS,
        background: "transparent",
        lineHeight: 1,
        transform: "translate(50%, -50%)",
        fontSize: e.fontSize,
        cursor: "pointer",
        opacity: e.opacityLoading,
        display: "none",
        "&:dir(rtl)": {
          transform: "translate(-50%, -50%)"
        },
        "&:hover": {
          opacity: 1
        },
        "&:active": {
          opacity: e.opacityLoading
        }
      },
      [`&:hover ${r}-remove`]: {
        display: "block"
      },
      // ============================== Status ===============================
      "&-status-error": {
        borderColor: e.colorError,
        [`${r}-desc`]: {
          color: e.colorError
        }
      },
      // ============================== Motion ===============================
      "&-motion": {
        transition: ["opacity", "width", "margin", "padding"].map((s) => `${s} ${e.motionDurationSlow}`).join(","),
        "&-appear-start": {
          width: 0,
          transition: "none"
        },
        "&-leave-active": {
          opacity: 0,
          width: 0,
          paddingInline: 0,
          borderInlineWidth: 0,
          marginInlineEnd: n(e.paddingSM).mul(-1).equal()
        }
      }
    }
  };
}, un = {
  "&, *": {
    boxSizing: "border-box"
  }
}, ha = (e) => {
  const {
    componentCls: t,
    calc: n,
    antCls: r
  } = e, o = `${t}-drop-area`, s = `${t}-placeholder`;
  return {
    // ============================== Full Screen ==============================
    [o]: {
      position: "absolute",
      inset: 0,
      zIndex: e.zIndexPopupBase,
      ...un,
      "&-on-body": {
        position: "fixed",
        inset: 0
      },
      "&-hide-placement": {
        [`${s}-inner`]: {
          display: "none"
        }
      },
      [s]: {
        padding: 0
      }
    },
    "&": {
      // ============================= Placeholder =============================
      [s]: {
        height: "100%",
        borderRadius: e.borderRadius,
        borderWidth: e.lineWidthBold,
        borderStyle: "dashed",
        borderColor: "transparent",
        padding: e.padding,
        position: "relative",
        backdropFilter: "blur(10px)",
        background: e.colorBgPlaceholderHover,
        ...un,
        [`${r}-upload-wrapper ${r}-upload${r}-upload-btn`]: {
          padding: 0
        },
        [`&${s}-drag-in`]: {
          borderColor: e.colorPrimaryHover
        },
        [`&${s}-disabled`]: {
          opacity: 0.25,
          pointerEvents: "none"
        },
        [`${s}-inner`]: {
          gap: n(e.paddingXXS).div(2).equal()
        },
        [`${s}-icon`]: {
          fontSize: e.fontSizeHeading2,
          lineHeight: 1
        },
        [`${s}-title${s}-title`]: {
          margin: 0,
          fontSize: e.fontSize,
          lineHeight: e.lineHeight
        },
        [`${s}-description`]: {}
      }
    }
  };
}, ya = (e) => {
  const {
    componentCls: t,
    calc: n
  } = e, r = `${t}-list`, o = n(e.fontSize).mul(e.lineHeight).mul(2).add(e.paddingSM).add(e.paddingSM).equal();
  return {
    [t]: {
      position: "relative",
      width: "100%",
      ...un,
      // =============================== File List ===============================
      [r]: {
        display: "flex",
        flexWrap: "wrap",
        gap: e.paddingSM,
        fontSize: e.fontSize,
        lineHeight: e.lineHeight,
        color: e.colorText,
        paddingBlock: e.paddingSM,
        paddingInline: e.padding,
        width: "100%",
        background: e.colorBgContainer,
        // Hide scrollbar
        scrollbarWidth: "none",
        "-ms-overflow-style": "none",
        "&::-webkit-scrollbar": {
          display: "none"
        },
        // Scroll
        "&-overflow-scrollX, &-overflow-scrollY": {
          "&:before, &:after": {
            content: '""',
            position: "absolute",
            opacity: 0,
            transition: `opacity ${e.motionDurationSlow}`,
            zIndex: 1
          }
        },
        "&-overflow-ping-start:before": {
          opacity: 1
        },
        "&-overflow-ping-end:after": {
          opacity: 1
        },
        "&-overflow-scrollX": {
          overflowX: "auto",
          overflowY: "hidden",
          flexWrap: "nowrap",
          "&:before, &:after": {
            insetBlock: 0,
            width: 8
          },
          "&:before": {
            insetInlineStart: 0,
            background: "linear-gradient(to right, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          },
          "&:after": {
            insetInlineEnd: 0,
            background: "linear-gradient(to left, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          },
          "&:dir(rtl)": {
            "&:before": {
              background: "linear-gradient(to left, rgba(0,0,0,0.06), rgba(0,0,0,0));"
            },
            "&:after": {
              background: "linear-gradient(to right, rgba(0,0,0,0.06), rgba(0,0,0,0));"
            }
          }
        },
        "&-overflow-scrollY": {
          overflowX: "hidden",
          overflowY: "auto",
          maxHeight: n(o).mul(3).equal(),
          "&:before, &:after": {
            insetInline: 0,
            height: 8
          },
          "&:before": {
            insetBlockStart: 0,
            background: "linear-gradient(to bottom, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          },
          "&:after": {
            insetBlockEnd: 0,
            background: "linear-gradient(to top, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          }
        },
        // ======================================================================
        // ==                              Upload                              ==
        // ======================================================================
        "&-upload-btn": {
          width: o,
          height: o,
          fontSize: e.fontSizeHeading2,
          color: "#999"
        },
        // ======================================================================
        // ==                             PrevNext                             ==
        // ======================================================================
        "&-prev-btn, &-next-btn": {
          position: "absolute",
          top: "50%",
          transform: "translateY(-50%)",
          boxShadow: e.boxShadowTertiary,
          opacity: 0,
          pointerEvents: "none"
        },
        "&-prev-btn": {
          left: {
            _skip_check_: !0,
            value: e.padding
          }
        },
        "&-next-btn": {
          right: {
            _skip_check_: !0,
            value: e.padding
          }
        },
        "&:dir(ltr)": {
          [`&${r}-overflow-ping-start ${r}-prev-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          },
          [`&${r}-overflow-ping-end ${r}-next-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          }
        },
        "&:dir(rtl)": {
          [`&${r}-overflow-ping-end ${r}-prev-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          },
          [`&${r}-overflow-ping-start ${r}-next-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          }
        }
      }
    }
  };
}, va = (e) => {
  const {
    colorBgContainer: t
  } = e;
  return {
    colorBgPlaceholderHover: new ye(t).setA(0.85).toRgbString()
  };
}, fo = kt("Attachments", (e) => {
  const t = Ke(e, {});
  return [ha(t), ya(t), ga(t)];
}, va), ba = (e) => e.indexOf("image/") === 0, ut = 200;
function Sa(e) {
  return new Promise((t) => {
    if (!e || !e.type || !ba(e.type)) {
      t("");
      return;
    }
    const n = new Image();
    if (n.onload = () => {
      const {
        width: r,
        height: o
      } = n, s = r / o, i = s > 1 ? ut : ut * s, a = s > 1 ? ut / s : ut, l = document.createElement("canvas");
      l.width = i, l.height = a, l.style.cssText = `position: fixed; left: 0; top: 0; width: ${i}px; height: ${a}px; z-index: 9999; display: none;`, document.body.appendChild(l), l.getContext("2d").drawImage(n, 0, 0, i, a);
      const f = l.toDataURL();
      document.body.removeChild(l), window.URL.revokeObjectURL(n.src), t(f);
    }, n.crossOrigin = "anonymous", e.type.startsWith("image/svg+xml")) {
      const r = new FileReader();
      r.onload = () => {
        r.result && typeof r.result == "string" && (n.src = r.result);
      }, r.readAsDataURL(e);
    } else if (e.type.startsWith("image/gif")) {
      const r = new FileReader();
      r.onload = () => {
        r.result && t(r.result);
      }, r.readAsDataURL(e);
    } else
      n.src = window.URL.createObjectURL(e);
  });
}
function xa() {
  return /* @__PURE__ */ c.createElement("svg", {
    width: "1em",
    height: "1em",
    viewBox: "0 0 16 16",
    version: "1.1",
    xmlns: "http://www.w3.org/2000/svg"
    //xmlnsXlink="http://www.w3.org/1999/xlink"
  }, /* @__PURE__ */ c.createElement("title", null, "audio"), /* @__PURE__ */ c.createElement("g", {
    stroke: "none",
    strokeWidth: "1",
    fill: "none",
    fillRule: "evenodd"
  }, /* @__PURE__ */ c.createElement("path", {
    d: "M14.1178571,4.0125 C14.225,4.11964286 14.2857143,4.26428571 14.2857143,4.41607143 L14.2857143,15.4285714 C14.2857143,15.7446429 14.0303571,16 13.7142857,16 L2.28571429,16 C1.96964286,16 1.71428571,15.7446429 1.71428571,15.4285714 L1.71428571,0.571428571 C1.71428571,0.255357143 1.96964286,0 2.28571429,0 L9.86964286,0 C10.0214286,0 10.1678571,0.0607142857 10.275,0.167857143 L14.1178571,4.0125 Z M10.7315824,7.11216117 C10.7428131,7.15148751 10.7485063,7.19218979 10.7485063,7.23309113 L10.7485063,8.07742614 C10.7484199,8.27364959 10.6183424,8.44607275 10.4296853,8.50003683 L8.32984514,9.09986306 L8.32984514,11.7071803 C8.32986605,12.5367078 7.67249692,13.217028 6.84345686,13.2454634 L6.79068592,13.2463395 C6.12766108,13.2463395 5.53916361,12.8217001 5.33010655,12.1924966 C5.1210495,11.563293 5.33842118,10.8709227 5.86959669,10.4741173 C6.40077221,10.0773119 7.12636292,10.0652587 7.67042486,10.4442027 L7.67020842,7.74937024 L7.68449368,7.74937024 C7.72405122,7.59919041 7.83988806,7.48101083 7.98924584,7.4384546 L10.1880418,6.81004755 C10.42156,6.74340323 10.6648954,6.87865515 10.7315824,7.11216117 Z M9.60714286,1.31785714 L12.9678571,4.67857143 L9.60714286,4.67857143 L9.60714286,1.31785714 Z",
    fill: "currentColor"
  })));
}
function wa(e) {
  const {
    percent: t
  } = e, {
    token: n
  } = We.useToken();
  return /* @__PURE__ */ c.createElement(is, {
    type: "circle",
    percent: t,
    size: n.fontSizeHeading2 * 2,
    strokeColor: "#FFF",
    trailColor: "rgba(255, 255, 255, 0.3)",
    format: (r) => /* @__PURE__ */ c.createElement("span", {
      style: {
        color: "#FFF"
      }
    }, (r || 0).toFixed(0), "%")
  });
}
function _a() {
  return /* @__PURE__ */ c.createElement("svg", {
    width: "1em",
    height: "1em",
    viewBox: "0 0 16 16",
    version: "1.1",
    xmlns: "http://www.w3.org/2000/svg"
    // xmlnsXlink="http://www.w3.org/1999/xlink"
  }, /* @__PURE__ */ c.createElement("title", null, "video"), /* @__PURE__ */ c.createElement("g", {
    stroke: "none",
    strokeWidth: "1",
    fill: "none",
    fillRule: "evenodd"
  }, /* @__PURE__ */ c.createElement("path", {
    d: "M14.1178571,4.0125 C14.225,4.11964286 14.2857143,4.26428571 14.2857143,4.41607143 L14.2857143,15.4285714 C14.2857143,15.7446429 14.0303571,16 13.7142857,16 L2.28571429,16 C1.96964286,16 1.71428571,15.7446429 1.71428571,15.4285714 L1.71428571,0.571428571 C1.71428571,0.255357143 1.96964286,0 2.28571429,0 L9.86964286,0 C10.0214286,0 10.1678571,0.0607142857 10.275,0.167857143 L14.1178571,4.0125 Z M12.9678571,4.67857143 L9.60714286,1.31785714 L9.60714286,4.67857143 L12.9678571,4.67857143 Z M10.5379461,10.3101106 L6.68957555,13.0059749 C6.59910784,13.0693494 6.47439406,13.0473861 6.41101953,12.9569184 C6.3874624,12.9232903 6.37482581,12.8832269 6.37482581,12.8421686 L6.37482581,7.45043999 C6.37482581,7.33998304 6.46436886,7.25043999 6.57482581,7.25043999 C6.61588409,7.25043999 6.65594753,7.26307658 6.68957555,7.28663371 L10.5379461,9.98249803 C10.6284138,10.0458726 10.6503772,10.1705863 10.5870027,10.2610541 C10.5736331,10.2801392 10.5570312,10.2967411 10.5379461,10.3101106 Z",
    fill: "currentColor"
  })));
}
const Zt = " ", dn = "#8c8c8c", mo = ["png", "jpg", "jpeg", "gif", "bmp", "webp", "svg"], Ea = [{
  icon: /* @__PURE__ */ c.createElement(Do, null),
  color: "#22b35e",
  ext: ["xlsx", "xls"]
}, {
  icon: /* @__PURE__ */ c.createElement(Ho, null),
  color: dn,
  ext: mo
}, {
  icon: /* @__PURE__ */ c.createElement(Bo, null),
  color: dn,
  ext: ["md", "mdx"]
}, {
  icon: /* @__PURE__ */ c.createElement(Wo, null),
  color: "#ff4d4f",
  ext: ["pdf"]
}, {
  icon: /* @__PURE__ */ c.createElement(Vo, null),
  color: "#ff6e31",
  ext: ["ppt", "pptx"]
}, {
  icon: /* @__PURE__ */ c.createElement(Xo, null),
  color: "#1677ff",
  ext: ["doc", "docx"]
}, {
  icon: /* @__PURE__ */ c.createElement(Uo, null),
  color: "#fab714",
  ext: ["zip", "rar", "7z", "tar", "gz"]
}, {
  icon: /* @__PURE__ */ c.createElement(_a, null),
  color: "#ff4d4f",
  ext: ["mp4", "avi", "mov", "wmv", "flv", "mkv"]
}, {
  icon: /* @__PURE__ */ c.createElement(xa, null),
  color: "#8c8c8c",
  ext: ["mp3", "wav", "flac", "ape", "aac", "ogg"]
}];
function yr(e, t) {
  return t.some((n) => e.toLowerCase() === `.${n}`);
}
function Ca(e) {
  let t = e;
  const n = ["B", "KB", "MB", "GB", "TB", "PB", "EB"];
  let r = 0;
  for (; t >= 1024 && r < n.length - 1; )
    t /= 1024, r++;
  return `${t.toFixed(0)} ${n[r]}`;
}
function Ta(e, t) {
  const {
    prefixCls: n,
    item: r,
    onRemove: o,
    className: s,
    style: i,
    imageProps: a
  } = e, l = c.useContext(rt), {
    disabled: u
  } = l || {}, {
    name: f,
    size: m,
    percent: d,
    status: h = "done",
    description: v
  } = r, {
    getPrefixCls: g
  } = $e(), p = g("attachment", n), y = `${p}-list-card`, [T, R, $] = fo(p), [E, x] = c.useMemo(() => {
    const F = f || "", D = F.match(/^(.*)\.[^.]+$/);
    return D ? [D[1], F.slice(D[1].length)] : [F, ""];
  }, [f]), I = c.useMemo(() => yr(x, mo), [x]), _ = c.useMemo(() => v || (h === "uploading" ? `${d || 0}%` : h === "error" ? r.response || Zt : m ? Ca(m) : Zt), [h, d]), [P, N] = c.useMemo(() => {
    for (const {
      ext: F,
      icon: D,
      color: W
    } of Ea)
      if (yr(x, F))
        return [D, W];
    return [/* @__PURE__ */ c.createElement(Ao, {
      key: "defaultIcon"
    }), dn];
  }, [x]), [z, k] = c.useState();
  c.useEffect(() => {
    if (r.originFileObj) {
      let F = !0;
      return Sa(r.originFileObj).then((D) => {
        F && k(D);
      }), () => {
        F = !1;
      };
    }
    k(void 0);
  }, [r.originFileObj]);
  let w = null;
  const b = r.thumbUrl || r.url || z, M = I && (r.originFileObj || b);
  return M ? w = /* @__PURE__ */ c.createElement(c.Fragment, null, b && /* @__PURE__ */ c.createElement(as, be({}, a, {
    alt: "preview",
    src: b
  })), h !== "done" && /* @__PURE__ */ c.createElement("div", {
    className: `${y}-img-mask`
  }, h === "uploading" && d !== void 0 && /* @__PURE__ */ c.createElement(wa, {
    percent: d,
    prefixCls: y
  }), h === "error" && /* @__PURE__ */ c.createElement("div", {
    className: `${y}-desc`
  }, /* @__PURE__ */ c.createElement("div", {
    className: `${y}-ellipsis-prefix`
  }, _)))) : w = /* @__PURE__ */ c.createElement(c.Fragment, null, /* @__PURE__ */ c.createElement("div", {
    className: `${y}-icon`,
    style: {
      color: N
    }
  }, P), /* @__PURE__ */ c.createElement("div", {
    className: `${y}-content`
  }, /* @__PURE__ */ c.createElement("div", {
    className: `${y}-name`
  }, /* @__PURE__ */ c.createElement("div", {
    className: `${y}-ellipsis-prefix`
  }, E ?? Zt), /* @__PURE__ */ c.createElement("div", {
    className: `${y}-ellipsis-suffix`
  }, x)), /* @__PURE__ */ c.createElement("div", {
    className: `${y}-desc`
  }, /* @__PURE__ */ c.createElement("div", {
    className: `${y}-ellipsis-prefix`
  }, _)))), T(/* @__PURE__ */ c.createElement("div", {
    className: j(y, {
      [`${y}-status-${h}`]: h,
      [`${y}-type-preview`]: M,
      [`${y}-type-overview`]: !M
    }, s, R, $),
    style: i,
    ref: t
  }, w, !u && o && /* @__PURE__ */ c.createElement("button", {
    type: "button",
    className: `${y}-remove`,
    onClick: () => {
      o(r);
    }
  }, /* @__PURE__ */ c.createElement(zo, null))));
}
const po = /* @__PURE__ */ c.forwardRef(Ta), vr = 1;
function $a(e) {
  const {
    prefixCls: t,
    items: n,
    onRemove: r,
    overflow: o,
    upload: s,
    listClassName: i,
    listStyle: a,
    itemClassName: l,
    itemStyle: u,
    imageProps: f
  } = e, m = `${t}-list`, d = c.useRef(null), [h, v] = c.useState(!1), {
    disabled: g
  } = c.useContext(rt);
  c.useEffect(() => (v(!0), () => {
    v(!1);
  }), []);
  const [p, y] = c.useState(!1), [T, R] = c.useState(!1), $ = () => {
    const _ = d.current;
    _ && (o === "scrollX" ? (y(Math.abs(_.scrollLeft) >= vr), R(_.scrollWidth - _.clientWidth - Math.abs(_.scrollLeft) >= vr)) : o === "scrollY" && (y(_.scrollTop !== 0), R(_.scrollHeight - _.clientHeight !== _.scrollTop)));
  };
  c.useEffect(() => {
    $();
  }, [o, n.length]);
  const E = (_) => {
    const P = d.current;
    P && P.scrollTo({
      left: P.scrollLeft + _ * P.clientWidth,
      behavior: "smooth"
    });
  }, x = () => {
    E(-1);
  }, I = () => {
    E(1);
  };
  return /* @__PURE__ */ c.createElement("div", {
    className: j(m, {
      [`${m}-overflow-${e.overflow}`]: o,
      [`${m}-overflow-ping-start`]: p,
      [`${m}-overflow-ping-end`]: T
    }, i),
    ref: d,
    onScroll: $,
    style: a
  }, /* @__PURE__ */ c.createElement(Ui, {
    keys: n.map((_) => ({
      key: _.uid,
      item: _
    })),
    motionName: `${m}-card-motion`,
    component: !1,
    motionAppear: h,
    motionLeave: !0,
    motionEnter: !0
  }, ({
    key: _,
    item: P,
    className: N,
    style: z
  }) => /* @__PURE__ */ c.createElement(po, {
    key: _,
    prefixCls: t,
    item: P,
    onRemove: r,
    className: j(N, l),
    imageProps: f,
    style: {
      ...z,
      ...u
    }
  })), !g && /* @__PURE__ */ c.createElement(io, {
    upload: s
  }, /* @__PURE__ */ c.createElement(se, {
    className: `${m}-upload-btn`,
    type: "dashed"
  }, /* @__PURE__ */ c.createElement(Go, {
    className: `${m}-upload-btn-icon`
  }))), o === "scrollX" && /* @__PURE__ */ c.createElement(c.Fragment, null, /* @__PURE__ */ c.createElement(se, {
    size: "small",
    shape: "circle",
    className: `${m}-prev-btn`,
    icon: /* @__PURE__ */ c.createElement(qo, null),
    onClick: x
  }), /* @__PURE__ */ c.createElement(se, {
    size: "small",
    shape: "circle",
    className: `${m}-next-btn`,
    icon: /* @__PURE__ */ c.createElement(Ko, null),
    onClick: I
  })));
}
function Ra(e, t) {
  const {
    prefixCls: n,
    placeholder: r = {},
    upload: o,
    className: s,
    style: i
  } = e, a = `${n}-placeholder`, l = r || {}, {
    disabled: u
  } = c.useContext(rt), [f, m] = c.useState(!1), d = () => {
    m(!0);
  }, h = (p) => {
    p.currentTarget.contains(p.relatedTarget) || m(!1);
  }, v = () => {
    m(!1);
  }, g = /* @__PURE__ */ c.isValidElement(r) ? r : /* @__PURE__ */ c.createElement(Ee, {
    align: "center",
    justify: "center",
    vertical: !0,
    className: `${a}-inner`
  }, /* @__PURE__ */ c.createElement(Te.Text, {
    className: `${a}-icon`
  }, l.icon), /* @__PURE__ */ c.createElement(Te.Title, {
    className: `${a}-title`,
    level: 5
  }, l.title), /* @__PURE__ */ c.createElement(Te.Text, {
    className: `${a}-description`,
    type: "secondary"
  }, l.description));
  return /* @__PURE__ */ c.createElement("div", {
    className: j(a, {
      [`${a}-drag-in`]: f,
      [`${a}-disabled`]: u
    }, s),
    onDragEnter: d,
    onDragLeave: h,
    onDrop: v,
    "aria-hidden": u,
    style: i
  }, /* @__PURE__ */ c.createElement(Nr.Dragger, be({
    showUploadList: !1
  }, o, {
    ref: t,
    style: {
      padding: 0,
      border: 0,
      background: "transparent"
    }
  }), g));
}
const Pa = /* @__PURE__ */ c.forwardRef(Ra);
function Ia(e, t) {
  const {
    prefixCls: n,
    rootClassName: r,
    rootStyle: o,
    className: s,
    style: i,
    items: a,
    children: l,
    getDropContainer: u,
    placeholder: f,
    onChange: m,
    onRemove: d,
    overflow: h,
    imageProps: v,
    disabled: g,
    classNames: p = {},
    styles: y = {},
    ...T
  } = e, {
    getPrefixCls: R,
    direction: $
  } = $e(), E = R("attachment", n), x = _t("attachments"), {
    classNames: I,
    styles: _
  } = x, P = c.useRef(null), N = c.useRef(null);
  c.useImperativeHandle(t, () => ({
    nativeElement: P.current,
    upload: (B) => {
      var V, q;
      const G = (q = (V = N.current) == null ? void 0 : V.nativeElement) == null ? void 0 : q.querySelector('input[type="file"]');
      if (G) {
        const Se = new DataTransfer();
        Se.items.add(B), G.files = Se.files, G.dispatchEvent(new Event("change", {
          bubbles: !0
        }));
      }
    }
  }));
  const [z, k, w] = fo(E), b = j(k, w), [M, F] = ci([], {
    value: a
  }), D = Re((B) => {
    F(B.fileList), m == null || m(B);
  }), W = {
    ...T,
    fileList: M,
    onChange: D
  }, re = (B) => Promise.resolve(typeof d == "function" ? d(B) : d).then((G) => {
    if (G === !1)
      return;
    const V = M.filter((q) => q.uid !== B.uid);
    D({
      file: {
        ...B,
        status: "removed"
      },
      fileList: V
    });
  });
  let te;
  const U = (B, G, V) => {
    const q = typeof f == "function" ? f(B) : f;
    return /* @__PURE__ */ c.createElement(Pa, {
      placeholder: q,
      upload: W,
      prefixCls: E,
      className: j(I.placeholder, p.placeholder),
      style: {
        ..._.placeholder,
        ...y.placeholder,
        ...G == null ? void 0 : G.style
      },
      ref: V
    });
  };
  if (l)
    te = /* @__PURE__ */ c.createElement(c.Fragment, null, /* @__PURE__ */ c.createElement(io, {
      upload: W,
      rootClassName: r,
      ref: N
    }, l), /* @__PURE__ */ c.createElement(tr, {
      getDropContainer: u,
      prefixCls: E,
      className: j(b, r)
    }, U("drop")));
  else {
    const B = M.length > 0;
    te = /* @__PURE__ */ c.createElement("div", {
      className: j(E, b, {
        [`${E}-rtl`]: $ === "rtl"
      }, s, r),
      style: {
        ...o,
        ...i
      },
      dir: $ || "ltr",
      ref: P
    }, /* @__PURE__ */ c.createElement($a, {
      prefixCls: E,
      items: M,
      onRemove: re,
      overflow: h,
      upload: W,
      listClassName: j(I.list, p.list),
      listStyle: {
        ..._.list,
        ...y.list,
        ...!B && {
          display: "none"
        }
      },
      itemClassName: j(I.item, p.item),
      itemStyle: {
        ..._.item,
        ...y.item
      },
      imageProps: v
    }), U("inline", B ? {
      style: {
        display: "none"
      }
    } : {}, N), /* @__PURE__ */ c.createElement(tr, {
      getDropContainer: u || (() => P.current),
      prefixCls: E,
      className: b
    }, U("drop")));
  }
  return z(/* @__PURE__ */ c.createElement(rt.Provider, {
    value: {
      disabled: g
    }
  }, te));
}
const go = /* @__PURE__ */ c.forwardRef(Ia);
go.FileCard = po;
var Ma = `accept acceptCharset accessKey action allowFullScreen allowTransparency
    alt async autoComplete autoFocus autoPlay capture cellPadding cellSpacing challenge
    charSet checked classID className colSpan cols content contentEditable contextMenu
    controls coords crossOrigin data dateTime default defer dir disabled download draggable
    encType form formAction formEncType formMethod formNoValidate formTarget frameBorder
    headers height hidden high href hrefLang htmlFor httpEquiv icon id inputMode integrity
    is keyParams keyType kind label lang list loop low manifest marginHeight marginWidth max maxLength media
    mediaGroup method min minLength multiple muted name noValidate nonce open
    optimum pattern placeholder poster preload radioGroup readOnly rel required
    reversed role rowSpan rows sandbox scope scoped scrolling seamless selected
    shape size sizes span spellCheck src srcDoc srcLang srcSet start step style
    summary tabIndex target title type useMap value width wmode wrap`, La = `onCopy onCut onPaste onCompositionEnd onCompositionStart onCompositionUpdate onKeyDown
    onKeyPress onKeyUp onFocus onBlur onChange onInput onSubmit onClick onContextMenu onDoubleClick
    onDrag onDragEnd onDragEnter onDragExit onDragLeave onDragOver onDragStart onDrop onMouseDown
    onMouseEnter onMouseLeave onMouseMove onMouseOut onMouseOver onMouseUp onSelect onTouchCancel
    onTouchEnd onTouchMove onTouchStart onScroll onWheel onAbort onCanPlay onCanPlayThrough
    onDurationChange onEmptied onEncrypted onEnded onError onLoadedData onLoadedMetadata
    onLoadStart onPause onPlay onPlaying onProgress onRateChange onSeeked onSeeking onStalled onSuspend onTimeUpdate onVolumeChange onWaiting onLoad onError`, Na = "".concat(Ma, " ").concat(La).split(/[\s\n]+/), Fa = "aria-", Oa = "data-";
function br(e, t) {
  return e.indexOf(t) === 0;
}
function ja(e) {
  var t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !1, n;
  t === !1 ? n = {
    aria: !0,
    data: !0,
    attr: !0
  } : t === !0 ? n = {
    aria: !0
  } : n = O({}, t);
  var r = {};
  return Object.keys(e).forEach(function(o) {
    // Aria
    (n.aria && (o === "role" || br(o, Fa)) || // Data
    n.data && br(o, Oa) || // Attr
    n.attr && Na.includes(o)) && (r[o] = e[o]);
  }), r;
}
function dt(e) {
  return typeof e == "string";
}
const ka = (e, t, n, r) => {
  const o = L.useRef(""), [s, i] = L.useState(1), a = t && dt(e);
  return Br(() => {
    !a && dt(e) ? i(e.length) : dt(e) && dt(o.current) && e.indexOf(o.current) !== 0 && i(1), o.current = e;
  }, [e]), L.useEffect(() => {
    if (a && s < e.length) {
      const u = setTimeout(() => {
        i((f) => f + n);
      }, r);
      return () => {
        clearTimeout(u);
      };
    }
  }, [s, t, e]), [a ? e.slice(0, s) : e, a && s < e.length];
};
function Aa(e) {
  return L.useMemo(() => {
    if (!e)
      return [!1, 0, 0, null];
    let t = {
      step: 1,
      interval: 50,
      // set default suffix is empty
      suffix: null
    };
    return typeof e == "object" && (t = {
      ...t,
      ...e
    }), [!0, t.step, t.interval, t.suffix];
  }, [e]);
}
const za = ({
  prefixCls: e
}) => /* @__PURE__ */ c.createElement("span", {
  className: `${e}-dot`
}, /* @__PURE__ */ c.createElement("i", {
  className: `${e}-dot-item`,
  key: "item-1"
}), /* @__PURE__ */ c.createElement("i", {
  className: `${e}-dot-item`,
  key: "item-2"
}), /* @__PURE__ */ c.createElement("i", {
  className: `${e}-dot-item`,
  key: "item-3"
})), Da = (e) => {
  const {
    componentCls: t,
    paddingSM: n,
    padding: r
  } = e;
  return {
    [t]: {
      [`${t}-content`]: {
        // Shared: filled, outlined, shadow
        "&-filled,&-outlined,&-shadow": {
          padding: `${Ve(n)} ${Ve(r)}`,
          borderRadius: e.borderRadiusLG
        },
        // Filled:
        "&-filled": {
          backgroundColor: e.colorFillContent
        },
        // Outlined:
        "&-outlined": {
          border: `1px solid ${e.colorBorderSecondary}`
        },
        // Shadow:
        "&-shadow": {
          boxShadow: e.boxShadowTertiary
        }
      }
    }
  };
}, Ha = (e) => {
  const {
    componentCls: t,
    fontSize: n,
    lineHeight: r,
    paddingSM: o,
    padding: s,
    calc: i
  } = e, a = i(n).mul(r).div(2).add(o).equal(), l = `${t}-content`;
  return {
    [t]: {
      [l]: {
        // round:
        "&-round": {
          borderRadius: {
            _skip_check_: !0,
            value: a
          },
          paddingInline: i(s).mul(1.25).equal()
        }
      },
      // corner:
      [`&-start ${l}-corner`]: {
        borderStartStartRadius: e.borderRadiusXS
      },
      [`&-end ${l}-corner`]: {
        borderStartEndRadius: e.borderRadiusXS
      }
    }
  };
}, Ba = (e) => {
  const {
    componentCls: t,
    padding: n
  } = e;
  return {
    [`${t}-list`]: {
      display: "flex",
      flexDirection: "column",
      gap: n,
      overflowY: "auto"
    }
  };
}, Wa = new Or("loadingMove", {
  "0%": {
    transform: "translateY(0)"
  },
  "10%": {
    transform: "translateY(4px)"
  },
  "20%": {
    transform: "translateY(0)"
  },
  "30%": {
    transform: "translateY(-4px)"
  },
  "40%": {
    transform: "translateY(0)"
  }
}), Va = new Or("cursorBlink", {
  "0%": {
    opacity: 1
  },
  "50%": {
    opacity: 0
  },
  "100%": {
    opacity: 1
  }
}), Xa = (e) => {
  const {
    componentCls: t,
    fontSize: n,
    lineHeight: r,
    paddingSM: o,
    colorText: s,
    calc: i
  } = e;
  return {
    [t]: {
      display: "flex",
      columnGap: o,
      [`&${t}-end`]: {
        justifyContent: "end",
        flexDirection: "row-reverse",
        [`& ${t}-content-wrapper`]: {
          alignItems: "flex-end"
        }
      },
      [`&${t}-rtl`]: {
        direction: "rtl"
      },
      [`&${t}-typing ${t}-content:last-child::after`]: {
        content: '"|"',
        fontWeight: 900,
        userSelect: "none",
        opacity: 1,
        marginInlineStart: "0.1em",
        animationName: Va,
        animationDuration: "0.8s",
        animationIterationCount: "infinite",
        animationTimingFunction: "linear"
      },
      // ============================ Avatar =============================
      [`& ${t}-avatar`]: {
        display: "inline-flex",
        justifyContent: "center",
        alignSelf: "flex-start"
      },
      // ======================== Header & Footer ========================
      [`& ${t}-header, & ${t}-footer`]: {
        fontSize: n,
        lineHeight: r,
        color: e.colorText
      },
      [`& ${t}-header`]: {
        marginBottom: e.paddingXXS
      },
      [`& ${t}-footer`]: {
        marginTop: o
      },
      // =========================== Content =============================
      [`& ${t}-content-wrapper`]: {
        flex: "auto",
        display: "flex",
        flexDirection: "column",
        alignItems: "flex-start",
        minWidth: 0,
        maxWidth: "100%"
      },
      [`& ${t}-content`]: {
        position: "relative",
        boxSizing: "border-box",
        minWidth: 0,
        maxWidth: "100%",
        color: s,
        fontSize: e.fontSize,
        lineHeight: e.lineHeight,
        minHeight: i(o).mul(2).add(i(r).mul(n)).equal(),
        wordBreak: "break-word",
        [`& ${t}-dot`]: {
          position: "relative",
          height: "100%",
          display: "flex",
          alignItems: "center",
          columnGap: e.marginXS,
          padding: `0 ${Ve(e.paddingXXS)}`,
          "&-item": {
            backgroundColor: e.colorPrimary,
            borderRadius: "100%",
            width: 4,
            height: 4,
            animationName: Wa,
            animationDuration: "2s",
            animationIterationCount: "infinite",
            animationTimingFunction: "linear",
            "&:nth-child(1)": {
              animationDelay: "0s"
            },
            "&:nth-child(2)": {
              animationDelay: "0.2s"
            },
            "&:nth-child(3)": {
              animationDelay: "0.4s"
            }
          }
        }
      }
    }
  };
}, Ua = () => ({}), ho = kt("Bubble", (e) => {
  const t = Ke(e, {});
  return [Xa(t), Ba(t), Da(t), Ha(t)];
}, Ua), yo = /* @__PURE__ */ c.createContext({}), Ga = (e, t) => {
  const {
    prefixCls: n,
    className: r,
    rootClassName: o,
    style: s,
    classNames: i = {},
    styles: a = {},
    avatar: l,
    placement: u = "start",
    loading: f = !1,
    loadingRender: m,
    typing: d,
    content: h = "",
    messageRender: v,
    variant: g = "filled",
    shape: p,
    onTypingComplete: y,
    header: T,
    footer: R,
    ...$
  } = e, {
    onUpdate: E
  } = c.useContext(yo), x = c.useRef(null);
  c.useImperativeHandle(t, () => ({
    nativeElement: x.current
  }));
  const {
    direction: I,
    getPrefixCls: _
  } = $e(), P = _("bubble", n), N = _t("bubble"), [z, k, w, b] = Aa(d), [M, F] = ka(h, z, k, w);
  c.useEffect(() => {
    E == null || E();
  }, [M]);
  const D = c.useRef(!1);
  c.useEffect(() => {
    !F && !f ? D.current || (D.current = !0, y == null || y()) : D.current = !1;
  }, [F, f]);
  const [W, re, te] = ho(P), U = j(P, o, N.className, r, re, te, `${P}-${u}`, {
    [`${P}-rtl`]: I === "rtl",
    [`${P}-typing`]: F && !f && !v && !b
  }), B = /* @__PURE__ */ c.isValidElement(l) ? l : /* @__PURE__ */ c.createElement(ls, l), G = v ? v(M) : M;
  let V;
  f ? V = m ? m() : /* @__PURE__ */ c.createElement(za, {
    prefixCls: P
  }) : V = /* @__PURE__ */ c.createElement(c.Fragment, null, G, F && b);
  let q = /* @__PURE__ */ c.createElement("div", {
    style: {
      ...N.styles.content,
      ...a.content
    },
    className: j(`${P}-content`, `${P}-content-${g}`, p && `${P}-content-${p}`, N.classNames.content, i.content)
  }, V);
  return (T || R) && (q = /* @__PURE__ */ c.createElement("div", {
    className: `${P}-content-wrapper`
  }, T && /* @__PURE__ */ c.createElement("div", {
    className: j(`${P}-header`, N.classNames.header, i.header),
    style: {
      ...N.styles.header,
      ...a.header
    }
  }, T), q, R && /* @__PURE__ */ c.createElement("div", {
    className: j(`${P}-footer`, N.classNames.footer, i.footer),
    style: {
      ...N.styles.footer,
      ...a.footer
    }
  }, R))), W(/* @__PURE__ */ c.createElement("div", be({
    style: {
      ...N.style,
      ...s
    },
    className: U
  }, $, {
    ref: x
  }), l && /* @__PURE__ */ c.createElement("div", {
    style: {
      ...N.styles.avatar,
      ...a.avatar
    },
    className: j(`${P}-avatar`, N.classNames.avatar, i.avatar)
  }, B), q));
}, En = /* @__PURE__ */ c.forwardRef(Ga);
function qa(e) {
  const [t, n] = c.useState(e.length), r = c.useMemo(() => e.slice(0, t), [e, t]), o = c.useMemo(() => {
    const i = r[r.length - 1];
    return i ? i.key : null;
  }, [r]);
  c.useEffect(() => {
    var i;
    if (!(r.length && r.every((a, l) => {
      var u;
      return a.key === ((u = e[l]) == null ? void 0 : u.key);
    }))) {
      if (r.length === 0)
        n(1);
      else
        for (let a = 0; a < r.length; a += 1)
          if (r[a].key !== ((i = e[a]) == null ? void 0 : i.key)) {
            n(a);
            break;
          }
    }
  }, [e]);
  const s = Re((i) => {
    i === o && n(t + 1);
  });
  return [r, s];
}
function Ka(e, t) {
  const n = L.useCallback((r, o) => typeof t == "function" ? t(r, o) : t ? t[r.role] || {} : {}, [t]);
  return L.useMemo(() => (e || []).map((r, o) => {
    const s = r.key ?? `preset_${o}`;
    return {
      ...n(r, o),
      ...r,
      key: s
    };
  }), [e, n]);
}
const Ya = 1, Qa = (e, t) => {
  const {
    prefixCls: n,
    rootClassName: r,
    className: o,
    items: s,
    autoScroll: i = !0,
    roles: a,
    ...l
  } = e, u = ja(l, {
    attr: !0,
    aria: !0
  }), f = L.useRef(null), m = L.useRef({}), {
    getPrefixCls: d
  } = $e(), h = d("bubble", n), v = `${h}-list`, [g, p, y] = ho(h), [T, R] = L.useState(!1);
  L.useEffect(() => (R(!0), () => {
    R(!1);
  }), []);
  const $ = Ka(s, a), [E, x] = qa($), [I, _] = L.useState(!0), [P, N] = L.useState(0), z = (b) => {
    const M = b.target;
    _(M.scrollHeight - Math.abs(M.scrollTop) - M.clientHeight <= Ya);
  };
  L.useEffect(() => {
    i && f.current && I && f.current.scrollTo({
      top: f.current.scrollHeight
    });
  }, [P]), L.useEffect(() => {
    var b;
    if (i) {
      const M = (b = E[E.length - 2]) == null ? void 0 : b.key, F = m.current[M];
      if (F) {
        const {
          nativeElement: D
        } = F, {
          top: W,
          bottom: re
        } = D.getBoundingClientRect(), {
          top: te,
          bottom: U
        } = f.current.getBoundingClientRect();
        W < U && re > te && (N((G) => G + 1), _(!0));
      }
    }
  }, [E.length]), L.useImperativeHandle(t, () => ({
    nativeElement: f.current,
    scrollTo: ({
      key: b,
      offset: M,
      behavior: F = "smooth",
      block: D
    }) => {
      if (typeof M == "number")
        f.current.scrollTo({
          top: M,
          behavior: F
        });
      else if (b !== void 0) {
        const W = m.current[b];
        if (W) {
          const re = E.findIndex((te) => te.key === b);
          _(re === E.length - 1), W.nativeElement.scrollIntoView({
            behavior: F,
            block: D
          });
        }
      }
    }
  }));
  const k = Re(() => {
    i && N((b) => b + 1);
  }), w = L.useMemo(() => ({
    onUpdate: k
  }), []);
  return g(/* @__PURE__ */ L.createElement(yo.Provider, {
    value: w
  }, /* @__PURE__ */ L.createElement("div", be({}, u, {
    className: j(v, r, o, p, y, {
      [`${v}-reach-end`]: I
    }),
    ref: f,
    onScroll: z
  }), E.map(({
    key: b,
    ...M
  }) => /* @__PURE__ */ L.createElement(En, be({}, M, {
    key: b,
    ref: (F) => {
      F ? m.current[b] = F : delete m.current[b];
    },
    typing: T ? M.typing : !1,
    onTypingComplete: () => {
      var F;
      (F = M.onTypingComplete) == null || F.call(M), x(b);
    }
  }))))));
}, Za = /* @__PURE__ */ L.forwardRef(Qa);
En.List = Za;
const Ja = (e) => {
  const {
    componentCls: t
  } = e;
  return {
    [t]: {
      // ======================== Prompt ========================
      "&, & *": {
        boxSizing: "border-box"
      },
      maxWidth: "100%",
      [`&${t}-rtl`]: {
        direction: "rtl"
      },
      [`& ${t}-title`]: {
        marginBlockStart: 0,
        fontWeight: "normal",
        color: e.colorTextTertiary
      },
      [`& ${t}-list`]: {
        display: "flex",
        gap: e.paddingSM,
        overflowX: "scroll",
        "&::-webkit-scrollbar": {
          display: "none"
        },
        listStyle: "none",
        paddingInlineStart: 0,
        marginBlock: 0,
        alignItems: "stretch",
        "&-wrap": {
          flexWrap: "wrap"
        },
        "&-vertical": {
          flexDirection: "column",
          alignItems: "flex-start"
        }
      },
      // ========================= Item =========================
      [`${t}-item`]: {
        flex: "none",
        display: "flex",
        gap: e.paddingXS,
        height: "auto",
        paddingBlock: e.paddingSM,
        paddingInline: e.padding,
        alignItems: "flex-start",
        justifyContent: "flex-start",
        background: e.colorBgContainer,
        borderRadius: e.borderRadiusLG,
        transition: ["border", "background"].map((n) => `${n} ${e.motionDurationSlow}`).join(","),
        border: `${Ve(e.lineWidth)} ${e.lineType} ${e.colorBorderSecondary}`,
        [`&:not(${t}-item-has-nest)`]: {
          "&:hover": {
            cursor: "pointer",
            background: e.colorFillTertiary
          },
          "&:active": {
            background: e.colorFill
          }
        },
        [`${t}-content`]: {
          flex: "auto",
          minWidth: 0,
          display: "flex",
          gap: e.paddingXXS,
          flexDirection: "column",
          alignItems: "flex-start"
        },
        [`${t}-icon, ${t}-label, ${t}-desc`]: {
          margin: 0,
          padding: 0,
          fontSize: e.fontSize,
          lineHeight: e.lineHeight,
          textAlign: "start",
          whiteSpace: "normal"
        },
        [`${t}-label`]: {
          color: e.colorTextHeading,
          fontWeight: 500
        },
        [`${t}-label + ${t}-desc`]: {
          color: e.colorTextTertiary
        },
        // Disabled
        [`&${t}-item-disabled`]: {
          pointerEvents: "none",
          background: e.colorBgContainerDisabled,
          [`${t}-label, ${t}-desc`]: {
            color: e.colorTextTertiary
          }
        }
      }
    }
  };
}, el = (e) => {
  const {
    componentCls: t
  } = e;
  return {
    [t]: {
      // ========================= Parent =========================
      [`${t}-item-has-nest`]: {
        [`> ${t}-content`]: {
          // gap: token.paddingSM,
          [`> ${t}-label`]: {
            fontSize: e.fontSizeLG,
            lineHeight: e.lineHeightLG
          }
        }
      },
      // ========================= Nested =========================
      [`&${t}-nested`]: {
        marginTop: e.paddingXS,
        // ======================== Prompt ========================
        alignSelf: "stretch",
        [`${t}-list`]: {
          alignItems: "stretch"
        },
        // ========================= Item =========================
        [`${t}-item`]: {
          border: 0,
          background: e.colorFillQuaternary
        }
      }
    }
  };
}, tl = () => ({}), nl = kt("Prompts", (e) => {
  const t = Ke(e, {});
  return [Ja(t), el(t)];
}, tl), Cn = (e) => {
  const {
    prefixCls: t,
    title: n,
    className: r,
    items: o,
    onItemClick: s,
    vertical: i,
    wrap: a,
    rootClassName: l,
    styles: u = {},
    classNames: f = {},
    style: m,
    ...d
  } = e, {
    getPrefixCls: h,
    direction: v
  } = $e(), g = h("prompts", t), p = _t("prompts"), [y, T, R] = nl(g), $ = j(g, p.className, r, l, T, R, {
    [`${g}-rtl`]: v === "rtl"
  }), E = j(`${g}-list`, p.classNames.list, f.list, {
    [`${g}-list-wrap`]: a
  }, {
    [`${g}-list-vertical`]: i
  });
  return y(/* @__PURE__ */ c.createElement("div", be({}, d, {
    className: $,
    style: {
      ...m,
      ...p.style
    }
  }), n && /* @__PURE__ */ c.createElement(Te.Title, {
    level: 5,
    className: j(`${g}-title`, p.classNames.title, f.title),
    style: {
      ...p.styles.title,
      ...u.title
    }
  }, n), /* @__PURE__ */ c.createElement("div", {
    className: E,
    style: {
      ...p.styles.list,
      ...u.list
    }
  }, o == null ? void 0 : o.map((x, I) => {
    const _ = x.children && x.children.length > 0;
    return /* @__PURE__ */ c.createElement("div", {
      key: x.key || `key_${I}`,
      style: {
        ...p.styles.item,
        ...u.item
      },
      className: j(`${g}-item`, p.classNames.item, f.item, {
        [`${g}-item-disabled`]: x.disabled,
        [`${g}-item-has-nest`]: _
      }),
      onClick: () => {
        !_ && s && s({
          data: x
        });
      }
    }, x.icon && /* @__PURE__ */ c.createElement("div", {
      className: `${g}-icon`
    }, x.icon), /* @__PURE__ */ c.createElement("div", {
      className: j(`${g}-content`, p.classNames.itemContent, f.itemContent),
      style: {
        ...p.styles.itemContent,
        ...u.itemContent
      }
    }, x.label && /* @__PURE__ */ c.createElement("h6", {
      className: `${g}-label`
    }, x.label), x.description && /* @__PURE__ */ c.createElement("p", {
      className: `${g}-desc`
    }, x.description), _ && /* @__PURE__ */ c.createElement(Cn, {
      className: `${g}-nested`,
      items: x.children,
      vertical: !0,
      onItemClick: s,
      classNames: {
        list: f.subList,
        item: f.subItem
      },
      styles: {
        list: u.subList,
        item: u.subItem
      }
    })));
  }))));
}, rl = (e) => {
  const {
    componentCls: t,
    calc: n
  } = e, r = n(e.fontSizeHeading3).mul(e.lineHeightHeading3).equal(), o = n(e.fontSize).mul(e.lineHeight).equal();
  return {
    [t]: {
      gap: e.padding,
      // ======================== Icon ========================
      [`${t}-icon`]: {
        height: n(r).add(o).add(e.paddingXXS).equal(),
        display: "flex",
        img: {
          height: "100%"
        }
      },
      // ==================== Content Wrap ====================
      [`${t}-content-wrapper`]: {
        gap: e.paddingXS,
        flex: "auto",
        minWidth: 0,
        [`${t}-title-wrapper`]: {
          gap: e.paddingXS
        },
        [`${t}-title`]: {
          margin: 0
        },
        [`${t}-extra`]: {
          marginInlineStart: "auto"
        }
      }
    }
  };
}, ol = (e) => {
  const {
    componentCls: t
  } = e;
  return {
    [t]: {
      // ======================== Filled ========================
      "&-filled": {
        paddingInline: e.padding,
        paddingBlock: e.paddingSM,
        background: e.colorFillContent,
        borderRadius: e.borderRadiusLG
      },
      // ====================== Borderless ======================
      "&-borderless": {
        [`${t}-title`]: {
          fontSize: e.fontSizeHeading3,
          lineHeight: e.lineHeightHeading3
        }
      }
    }
  };
}, sl = () => ({}), il = kt("Welcome", (e) => {
  const t = Ke(e, {});
  return [rl(t), ol(t)];
}, sl);
function al(e, t) {
  const {
    prefixCls: n,
    rootClassName: r,
    className: o,
    style: s,
    variant: i = "filled",
    // Semantic
    classNames: a = {},
    styles: l = {},
    // Layout
    icon: u,
    title: f,
    description: m,
    extra: d
  } = e, {
    direction: h,
    getPrefixCls: v
  } = $e(), g = v("welcome", n), p = _t("welcome"), [y, T, R] = il(g), $ = c.useMemo(() => {
    if (!u)
      return null;
    let I = u;
    return typeof u == "string" && u.startsWith("http") && (I = /* @__PURE__ */ c.createElement("img", {
      src: u,
      alt: "icon"
    })), /* @__PURE__ */ c.createElement("div", {
      className: j(`${g}-icon`, p.classNames.icon, a.icon),
      style: l.icon
    }, I);
  }, [u]), E = c.useMemo(() => f ? /* @__PURE__ */ c.createElement(Te.Title, {
    level: 4,
    className: j(`${g}-title`, p.classNames.title, a.title),
    style: l.title
  }, f) : null, [f]), x = c.useMemo(() => d ? /* @__PURE__ */ c.createElement("div", {
    className: j(`${g}-extra`, p.classNames.extra, a.extra),
    style: l.extra
  }, d) : null, [d]);
  return y(/* @__PURE__ */ c.createElement(Ee, {
    ref: t,
    className: j(g, p.className, o, r, T, R, `${g}-${i}`, {
      [`${g}-rtl`]: h === "rtl"
    }),
    style: s
  }, $, /* @__PURE__ */ c.createElement(Ee, {
    vertical: !0,
    className: `${g}-content-wrapper`
  }, d ? /* @__PURE__ */ c.createElement(Ee, {
    align: "flex-start",
    className: `${g}-title-wrapper`
  }, E, x) : E, m && /* @__PURE__ */ c.createElement(Te.Text, {
    className: j(`${g}-description`, p.classNames.description, a.description),
    style: l.description
  }, m))));
}
const ll = /* @__PURE__ */ c.forwardRef(al);
function oe(e) {
  const t = J(e);
  return t.current = e, Lo((...n) => {
    var r;
    return (r = t.current) == null ? void 0 : r.call(t, ...n);
  }, []);
}
function he(e, t) {
  return Object.keys(e).reduce((n, r) => (e[r] !== void 0 && (!(t != null && t.omitNull) || e[r] !== null) && (n[r] = e[r]), n), {});
}
var vo = Symbol.for("immer-nothing"), Sr = Symbol.for("immer-draftable"), ae = Symbol.for("immer-state");
function ge(e, ...t) {
  throw new Error(`[Immer] minified error nr: ${e}. Full error at: https://bit.ly/3cXEKWf`);
}
var Xe = Object.getPrototypeOf;
function Ue(e) {
  return !!e && !!e[ae];
}
function Ne(e) {
  var t;
  return e ? bo(e) || Array.isArray(e) || !!e[Sr] || !!((t = e.constructor) != null && t[Sr]) || zt(e) || Dt(e) : !1;
}
var cl = Object.prototype.constructor.toString();
function bo(e) {
  if (!e || typeof e != "object") return !1;
  const t = Xe(e);
  if (t === null)
    return !0;
  const n = Object.hasOwnProperty.call(t, "constructor") && t.constructor;
  return n === Object ? !0 : typeof n == "function" && Function.toString.call(n) === cl;
}
function bt(e, t) {
  At(e) === 0 ? Reflect.ownKeys(e).forEach((n) => {
    t(n, e[n], e);
  }) : e.forEach((n, r) => t(r, n, e));
}
function At(e) {
  const t = e[ae];
  return t ? t.type_ : Array.isArray(e) ? 1 : zt(e) ? 2 : Dt(e) ? 3 : 0;
}
function fn(e, t) {
  return At(e) === 2 ? e.has(t) : Object.prototype.hasOwnProperty.call(e, t);
}
function So(e, t, n) {
  const r = At(e);
  r === 2 ? e.set(t, n) : r === 3 ? e.add(n) : e[t] = n;
}
function ul(e, t) {
  return e === t ? e !== 0 || 1 / e === 1 / t : e !== e && t !== t;
}
function zt(e) {
  return e instanceof Map;
}
function Dt(e) {
  return e instanceof Set;
}
function Me(e) {
  return e.copy_ || e.base_;
}
function mn(e, t) {
  if (zt(e))
    return new Map(e);
  if (Dt(e))
    return new Set(e);
  if (Array.isArray(e)) return Array.prototype.slice.call(e);
  const n = bo(e);
  if (t === !0 || t === "class_only" && !n) {
    const r = Object.getOwnPropertyDescriptors(e);
    delete r[ae];
    let o = Reflect.ownKeys(r);
    for (let s = 0; s < o.length; s++) {
      const i = o[s], a = r[i];
      a.writable === !1 && (a.writable = !0, a.configurable = !0), (a.get || a.set) && (r[i] = {
        configurable: !0,
        writable: !0,
        // could live with !!desc.set as well here...
        enumerable: a.enumerable,
        value: e[i]
      });
    }
    return Object.create(Xe(e), r);
  } else {
    const r = Xe(e);
    if (r !== null && n)
      return {
        ...e
      };
    const o = Object.create(r);
    return Object.assign(o, e);
  }
}
function Tn(e, t = !1) {
  return Ht(e) || Ue(e) || !Ne(e) || (At(e) > 1 && (e.set = e.add = e.clear = e.delete = dl), Object.freeze(e), t && Object.entries(e).forEach(([n, r]) => Tn(r, !0))), e;
}
function dl() {
  ge(2);
}
function Ht(e) {
  return Object.isFrozen(e);
}
var fl = {};
function Fe(e) {
  const t = fl[e];
  return t || ge(0, e), t;
}
var et;
function xo() {
  return et;
}
function ml(e, t) {
  return {
    drafts_: [],
    parent_: e,
    immer_: t,
    // Whenever the modified draft contains a draft from another scope, we
    // need to prevent auto-freezing so the unowned draft can be finalized.
    canAutoFreeze_: !0,
    unfinalizedDrafts_: 0
  };
}
function xr(e, t) {
  t && (Fe("Patches"), e.patches_ = [], e.inversePatches_ = [], e.patchListener_ = t);
}
function pn(e) {
  gn(e), e.drafts_.forEach(pl), e.drafts_ = null;
}
function gn(e) {
  e === et && (et = e.parent_);
}
function wr(e) {
  return et = ml(et, e);
}
function pl(e) {
  const t = e[ae];
  t.type_ === 0 || t.type_ === 1 ? t.revoke_() : t.revoked_ = !0;
}
function _r(e, t) {
  t.unfinalizedDrafts_ = t.drafts_.length;
  const n = t.drafts_[0];
  return e !== void 0 && e !== n ? (n[ae].modified_ && (pn(t), ge(4)), Ne(e) && (e = St(t, e), t.parent_ || xt(t, e)), t.patches_ && Fe("Patches").generateReplacementPatches_(n[ae].base_, e, t.patches_, t.inversePatches_)) : e = St(t, n, []), pn(t), t.patches_ && t.patchListener_(t.patches_, t.inversePatches_), e !== vo ? e : void 0;
}
function St(e, t, n) {
  if (Ht(t)) return t;
  const r = t[ae];
  if (!r)
    return bt(t, (o, s) => Er(e, r, t, o, s, n)), t;
  if (r.scope_ !== e) return t;
  if (!r.modified_)
    return xt(e, r.base_, !0), r.base_;
  if (!r.finalized_) {
    r.finalized_ = !0, r.scope_.unfinalizedDrafts_--;
    const o = r.copy_;
    let s = o, i = !1;
    r.type_ === 3 && (s = new Set(o), o.clear(), i = !0), bt(s, (a, l) => Er(e, r, o, a, l, n, i)), xt(e, o, !1), n && e.patches_ && Fe("Patches").generatePatches_(r, n, e.patches_, e.inversePatches_);
  }
  return r.copy_;
}
function Er(e, t, n, r, o, s, i) {
  if (Ue(o)) {
    const a = s && t && t.type_ !== 3 && // Set objects are atomic since they have no keys.
    !fn(t.assigned_, r) ? s.concat(r) : void 0, l = St(e, o, a);
    if (So(n, r, l), Ue(l))
      e.canAutoFreeze_ = !1;
    else return;
  } else i && n.add(o);
  if (Ne(o) && !Ht(o)) {
    if (!e.immer_.autoFreeze_ && e.unfinalizedDrafts_ < 1)
      return;
    St(e, o), (!t || !t.scope_.parent_) && typeof r != "symbol" && Object.prototype.propertyIsEnumerable.call(n, r) && xt(e, o);
  }
}
function xt(e, t, n = !1) {
  !e.parent_ && e.immer_.autoFreeze_ && e.canAutoFreeze_ && Tn(t, n);
}
function gl(e, t) {
  const n = Array.isArray(e), r = {
    type_: n ? 1 : 0,
    // Track which produce call this is associated with.
    scope_: t ? t.scope_ : xo(),
    // True for both shallow and deep changes.
    modified_: !1,
    // Used during finalization.
    finalized_: !1,
    // Track which properties have been assigned (true) or deleted (false).
    assigned_: {},
    // The parent draft state.
    parent_: t,
    // The base state.
    base_: e,
    // The base proxy.
    draft_: null,
    // set below
    // The base copy with any updated values.
    copy_: null,
    // Called by the `produce` function.
    revoke_: null,
    isManual_: !1
  };
  let o = r, s = $n;
  n && (o = [r], s = tt);
  const {
    revoke: i,
    proxy: a
  } = Proxy.revocable(o, s);
  return r.draft_ = a, r.revoke_ = i, a;
}
var $n = {
  get(e, t) {
    if (t === ae) return e;
    const n = Me(e);
    if (!fn(n, t))
      return hl(e, n, t);
    const r = n[t];
    return e.finalized_ || !Ne(r) ? r : r === Jt(e.base_, t) ? (en(e), e.copy_[t] = yn(r, e)) : r;
  },
  has(e, t) {
    return t in Me(e);
  },
  ownKeys(e) {
    return Reflect.ownKeys(Me(e));
  },
  set(e, t, n) {
    const r = wo(Me(e), t);
    if (r != null && r.set)
      return r.set.call(e.draft_, n), !0;
    if (!e.modified_) {
      const o = Jt(Me(e), t), s = o == null ? void 0 : o[ae];
      if (s && s.base_ === n)
        return e.copy_[t] = n, e.assigned_[t] = !1, !0;
      if (ul(n, o) && (n !== void 0 || fn(e.base_, t))) return !0;
      en(e), hn(e);
    }
    return e.copy_[t] === n && // special case: handle new props with value 'undefined'
    (n !== void 0 || t in e.copy_) || // special case: NaN
    Number.isNaN(n) && Number.isNaN(e.copy_[t]) || (e.copy_[t] = n, e.assigned_[t] = !0), !0;
  },
  deleteProperty(e, t) {
    return Jt(e.base_, t) !== void 0 || t in e.base_ ? (e.assigned_[t] = !1, en(e), hn(e)) : delete e.assigned_[t], e.copy_ && delete e.copy_[t], !0;
  },
  // Note: We never coerce `desc.value` into an Immer draft, because we can't make
  // the same guarantee in ES5 mode.
  getOwnPropertyDescriptor(e, t) {
    const n = Me(e), r = Reflect.getOwnPropertyDescriptor(n, t);
    return r && {
      writable: !0,
      configurable: e.type_ !== 1 || t !== "length",
      enumerable: r.enumerable,
      value: n[t]
    };
  },
  defineProperty() {
    ge(11);
  },
  getPrototypeOf(e) {
    return Xe(e.base_);
  },
  setPrototypeOf() {
    ge(12);
  }
}, tt = {};
bt($n, (e, t) => {
  tt[e] = function() {
    return arguments[0] = arguments[0][0], t.apply(this, arguments);
  };
});
tt.deleteProperty = function(e, t) {
  return tt.set.call(this, e, t, void 0);
};
tt.set = function(e, t, n) {
  return $n.set.call(this, e[0], t, n, e[0]);
};
function Jt(e, t) {
  const n = e[ae];
  return (n ? Me(n) : e)[t];
}
function hl(e, t, n) {
  var o;
  const r = wo(t, n);
  return r ? "value" in r ? r.value : (
    // This is a very special case, if the prop is a getter defined by the
    // prototype, we should invoke it with the draft as context!
    (o = r.get) == null ? void 0 : o.call(e.draft_)
  ) : void 0;
}
function wo(e, t) {
  if (!(t in e)) return;
  let n = Xe(e);
  for (; n; ) {
    const r = Object.getOwnPropertyDescriptor(n, t);
    if (r) return r;
    n = Xe(n);
  }
}
function hn(e) {
  e.modified_ || (e.modified_ = !0, e.parent_ && hn(e.parent_));
}
function en(e) {
  e.copy_ || (e.copy_ = mn(e.base_, e.scope_.immer_.useStrictShallowCopy_));
}
var yl = class {
  constructor(e) {
    this.autoFreeze_ = !0, this.useStrictShallowCopy_ = !1, this.produce = (t, n, r) => {
      if (typeof t == "function" && typeof n != "function") {
        const s = n;
        n = t;
        const i = this;
        return function(l = s, ...u) {
          return i.produce(l, (f) => n.call(this, f, ...u));
        };
      }
      typeof n != "function" && ge(6), r !== void 0 && typeof r != "function" && ge(7);
      let o;
      if (Ne(t)) {
        const s = wr(this), i = yn(t, void 0);
        let a = !0;
        try {
          o = n(i), a = !1;
        } finally {
          a ? pn(s) : gn(s);
        }
        return xr(s, r), _r(o, s);
      } else if (!t || typeof t != "object") {
        if (o = n(t), o === void 0 && (o = t), o === vo && (o = void 0), this.autoFreeze_ && Tn(o, !0), r) {
          const s = [], i = [];
          Fe("Patches").generateReplacementPatches_(t, o, s, i), r(s, i);
        }
        return o;
      } else ge(1, t);
    }, this.produceWithPatches = (t, n) => {
      if (typeof t == "function")
        return (i, ...a) => this.produceWithPatches(i, (l) => t(l, ...a));
      let r, o;
      return [this.produce(t, n, (i, a) => {
        r = i, o = a;
      }), r, o];
    }, typeof (e == null ? void 0 : e.autoFreeze) == "boolean" && this.setAutoFreeze(e.autoFreeze), typeof (e == null ? void 0 : e.useStrictShallowCopy) == "boolean" && this.setUseStrictShallowCopy(e.useStrictShallowCopy);
  }
  createDraft(e) {
    Ne(e) || ge(8), Ue(e) && (e = vl(e));
    const t = wr(this), n = yn(e, void 0);
    return n[ae].isManual_ = !0, gn(t), n;
  }
  finishDraft(e, t) {
    const n = e && e[ae];
    (!n || !n.isManual_) && ge(9);
    const {
      scope_: r
    } = n;
    return xr(r, t), _r(void 0, r);
  }
  /**
   * Pass true to automatically freeze all copies created by Immer.
   *
   * By default, auto-freezing is enabled.
   */
  setAutoFreeze(e) {
    this.autoFreeze_ = e;
  }
  /**
   * Pass true to enable strict shallow copy.
   *
   * By default, immer does not copy the object descriptors such as getter, setter and non-enumrable properties.
   */
  setUseStrictShallowCopy(e) {
    this.useStrictShallowCopy_ = e;
  }
  applyPatches(e, t) {
    let n;
    for (n = t.length - 1; n >= 0; n--) {
      const o = t[n];
      if (o.path.length === 0 && o.op === "replace") {
        e = o.value;
        break;
      }
    }
    n > -1 && (t = t.slice(n + 1));
    const r = Fe("Patches").applyPatches_;
    return Ue(e) ? r(e, t) : this.produce(e, (o) => r(o, t));
  }
};
function yn(e, t) {
  const n = zt(e) ? Fe("MapSet").proxyMap_(e, t) : Dt(e) ? Fe("MapSet").proxySet_(e, t) : gl(e, t);
  return (t ? t.scope_ : xo()).drafts_.push(n), n;
}
function vl(e) {
  return Ue(e) || ge(10, e), _o(e);
}
function _o(e) {
  if (!Ne(e) || Ht(e)) return e;
  const t = e[ae];
  let n;
  if (t) {
    if (!t.modified_) return t.base_;
    t.finalized_ = !0, n = mn(e, t.scope_.immer_.useStrictShallowCopy_);
  } else
    n = mn(e, !0);
  return bt(n, (r, o) => {
    So(n, r, _o(o));
  }), t && (t.finalized_ = !1), n;
}
var le = new yl(), Cr = le.produce;
le.produceWithPatches.bind(le);
le.setAutoFreeze.bind(le);
le.setUseStrictShallowCopy.bind(le);
le.applyPatches.bind(le);
le.createDraft.bind(le);
le.finishDraft.bind(le);
const {
  useItems: sc,
  withItemsContextProvider: ic,
  ItemHandler: ac
} = Fr("antdx-bubble.list-items"), {
  useItems: bl,
  withItemsContextProvider: Sl,
  ItemHandler: lc
} = Fr("antdx-bubble.list-roles");
function xl(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function wl(e, t = !1) {
  try {
    if (bn(e))
      return e;
    if (t && !xl(e))
      return;
    if (typeof e == "string") {
      let n = e.trim();
      return n.startsWith(";") && (n = n.slice(1)), n.endsWith(";") && (n = n.slice(0, -1)), new Function(`return (...args) => (${n})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function _l(e, t) {
  return ue(() => wl(e, t), [e, t]);
}
function El(e, t) {
  return t((r, o) => bn(r) ? o ? (...s) => r(...s, ...e) : r(...e) : r);
}
const Cl = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Tl(e) {
  return e ? Object.keys(e).reduce((t, n) => {
    const r = e[n];
    return t[n] = $l(n, r), t;
  }, {}) : {};
}
function $l(e, t) {
  return typeof t == "number" && !Cl.includes(e) ? t + "px" : t;
}
function vn(e) {
  const t = [], n = e.cloneNode(!1);
  if (e._reactElement) {
    const o = c.Children.toArray(e._reactElement.props.children).map((s) => {
      if (c.isValidElement(s) && s.props.__slot__) {
        const {
          portals: i,
          clonedElement: a
        } = vn(s.props.el);
        return c.cloneElement(s, {
          ...s.props,
          el: a,
          children: [...c.Children.toArray(s.props.children), ...i]
        });
      }
      return null;
    });
    return o.originalChildren = e._reactElement.props.children, t.push(ht(c.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: o
    }), n)), {
      clonedElement: n,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: i,
      type: a,
      useCapture: l
    }) => {
      n.addEventListener(a, i, l);
    });
  });
  const r = Array.from(e.childNodes);
  for (let o = 0; o < r.length; o++) {
    const s = r[o];
    if (s.nodeType === 1) {
      const {
        clonedElement: i,
        portals: a
      } = vn(s);
      t.push(...a), n.appendChild(i);
    } else s.nodeType === 3 && n.appendChild(s.cloneNode());
  }
  return {
    clonedElement: n,
    portals: t
  };
}
function Rl(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const Tr = No(({
  slot: e,
  clone: t,
  className: n,
  style: r,
  observeAttributes: o
}, s) => {
  const i = J(), [a, l] = Ze([]), {
    forceClone: u
  } = ms(), f = u ? !0 : t;
  return _e(() => {
    var g;
    if (!i.current || !e)
      return;
    let m = e;
    function d() {
      let p = m;
      if (m.tagName.toLowerCase() === "svelte-slot" && m.children.length === 1 && m.children[0] && (p = m.children[0], p.tagName.toLowerCase() === "react-portal-target" && p.children[0] && (p = p.children[0])), Rl(s, p), n && p.classList.add(...n.split(" ")), r) {
        const y = Tl(r);
        Object.keys(y).forEach((T) => {
          p.style[T] = y[T];
        });
      }
    }
    let h = null, v = null;
    if (f && window.MutationObserver) {
      let p = function() {
        var $, E, x;
        ($ = i.current) != null && $.contains(m) && ((E = i.current) == null || E.removeChild(m));
        const {
          portals: T,
          clonedElement: R
        } = vn(e);
        m = R, l(T), m.style.display = "contents", v && clearTimeout(v), v = setTimeout(() => {
          d();
        }, 50), (x = i.current) == null || x.appendChild(m);
      };
      p();
      const y = Rs(() => {
        p(), h == null || h.disconnect(), h == null || h.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: o
        });
      }, 50);
      h = new window.MutationObserver(y), h.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      m.style.display = "contents", d(), (g = i.current) == null || g.appendChild(m);
    return () => {
      var p, y;
      m.style.display = "", (p = i.current) != null && p.contains(m) && ((y = i.current) == null || y.removeChild(m)), h == null || h.disconnect();
    };
  }, [e, f, n, r, s, o, u]), c.createElement("react-child", {
    ref: i,
    style: {
      display: "contents"
    }
  }, ...a);
}), Pl = ({
  children: e,
  ...t
}) => /* @__PURE__ */ S.jsx(S.Fragment, {
  children: e(t)
});
function Il(e) {
  return c.createElement(Pl, {
    children: e
  });
}
function Eo(e, t, n) {
  const r = e.filter(Boolean);
  if (r.length !== 0)
    return r.map((o, s) => {
      var u;
      if (typeof o != "object")
        return t != null && t.fallback ? t.fallback(o) : o;
      const i = {
        ...o.props,
        key: ((u = o.props) == null ? void 0 : u.key) ?? (n ? `${n}-${s}` : `${s}`)
      };
      let a = i;
      Object.keys(o.slots).forEach((f) => {
        if (!o.slots[f] || !(o.slots[f] instanceof Element) && !o.slots[f].el)
          return;
        const m = f.split(".");
        m.forEach((y, T) => {
          a[y] || (a[y] = {}), T !== m.length - 1 && (a = i[y]);
        });
        const d = o.slots[f];
        let h, v, g = (t == null ? void 0 : t.clone) ?? !1, p = t == null ? void 0 : t.forceClone;
        d instanceof Element ? h = d : (h = d.el, v = d.callback, g = d.clone ?? g, p = d.forceClone ?? p), p = p ?? !!v, a[m[m.length - 1]] = h ? v ? (...y) => (v(m[m.length - 1], y), /* @__PURE__ */ S.jsx(zn, {
          ...o.ctx,
          params: y,
          forceClone: p,
          children: /* @__PURE__ */ S.jsx(Tr, {
            slot: h,
            clone: g
          })
        })) : Il((y) => /* @__PURE__ */ S.jsx(zn, {
          ...o.ctx,
          forceClone: p,
          children: /* @__PURE__ */ S.jsx(Tr, {
            ...y,
            slot: h,
            clone: g
          })
        })) : a[m[m.length - 1]], a = i;
      });
      const l = (t == null ? void 0 : t.children) || "children";
      return o[l] ? i[l] = Eo(o[l], t, `${s}`) : t != null && t.children && (i[l] = void 0, Reflect.deleteProperty(i, l)), i;
    });
}
const Co = Symbol();
function Ml(e, t) {
  return El(t, (n) => {
    var r, o;
    return {
      ...e,
      avatar: bn(e.avatar) ? n(e.avatar) : ve(e.avatar) ? {
        ...e.avatar,
        icon: n((r = e.avatar) == null ? void 0 : r.icon),
        src: n((o = e.avatar) == null ? void 0 : o.src)
      } : e.avatar,
      footer: n(e.footer),
      header: n(e.header),
      loadingRender: n(e.loadingRender, !0),
      messageRender: n(e.messageRender, !0)
    };
  });
}
function Ll({
  roles: e,
  preProcess: t,
  postProcess: n
}, r = []) {
  const o = _l(e), s = oe(t), i = oe(n), {
    items: {
      roles: a
    }
  } = bl(), l = ue(() => {
    var f;
    return e || ((f = Eo(a, {
      clone: !0,
      forceClone: !0
    })) == null ? void 0 : f.reduce((m, d) => (d.role !== void 0 && (m[d.role] = d), m), {}));
  }, [a, e]), u = ue(() => (f, m) => {
    const d = m ?? f[Co], h = s(f, d) || f;
    if (h.role && (l || {})[h.role])
      return Ml((l || {})[h.role], [h, d]);
    let v;
    return v = i(h, d), v || {
      messageRender(g) {
        return /* @__PURE__ */ S.jsx(S.Fragment, {
          children: ve(g) ? JSON.stringify(g) : g
        });
      }
    };
  }, [l, i, s, ...r]);
  return o || u;
}
function Nl(e) {
  const [t, n] = Ze(!1), r = J(0), o = J(!0), s = J(!0), {
    autoScroll: i,
    scrollButtonOffset: a,
    ref: l,
    value: u
  } = e, f = oe((d = "instant") => {
    l.current && (s.current = !0, requestAnimationFrame(() => {
      var h;
      (h = l.current) == null || h.scrollTo({
        offset: l.current.nativeElement.scrollHeight,
        behavior: d
      });
    }), n(!1));
  }), m = oe((d = 100) => {
    if (!l.current)
      return !1;
    const h = l.current.nativeElement, v = h.scrollHeight, {
      scrollTop: g,
      clientHeight: p
    } = h;
    return v - (g + p) < d;
  });
  return _e(() => {
    l.current && i && (u.length !== r.current && (o.current = !0), o.current && requestAnimationFrame(() => {
      f();
    }), r.current = u.length);
  }, [u, l, i, f, m]), _e(() => {
    if (l.current && i) {
      const d = l.current.nativeElement;
      let h = 0, v = 0;
      const g = (p) => {
        const y = p.target;
        s.current ? s.current = !1 : y.scrollTop < h && y.scrollHeight >= v ? o.current = !1 : m() && (o.current = !0), h = y.scrollTop, v = y.scrollHeight, n(!m(a));
      };
      return d.addEventListener("scroll", g), () => {
        d.removeEventListener("scroll", g);
      };
    }
  }, [i, m, a]), {
    showScrollButton: t,
    scrollToBottom: f
  };
}
new Intl.Collator(0, {
  numeric: 1
}).compare;
typeof process < "u" && process.versions && process.versions.node;
var we;
class cc extends TransformStream {
  /** Constructs a new instance. */
  constructor(n = {
    allowCR: !1
  }) {
    super({
      transform: (r, o) => {
        for (r = ze(this, we) + r; ; ) {
          const s = r.indexOf(`
`), i = n.allowCR ? r.indexOf("\r") : -1;
          if (i !== -1 && i !== r.length - 1 && (s === -1 || s - 1 > i)) {
            o.enqueue(r.slice(0, i)), r = r.slice(i + 1);
            continue;
          }
          if (s === -1) break;
          const a = r[s - 1] === "\r" ? s - 1 : s;
          o.enqueue(r.slice(0, a)), r = r.slice(s + 1);
        }
        jn(this, we, r);
      },
      flush: (r) => {
        if (ze(this, we) === "") return;
        const o = n.allowCR && ze(this, we).endsWith("\r") ? ze(this, we).slice(0, -1) : ze(this, we);
        r.enqueue(o);
      }
    });
    On(this, we, "");
  }
}
we = new WeakMap();
function Fl(e) {
  try {
    const t = new URL(e);
    return t.protocol === "http:" || t.protocol === "https:";
  } catch {
    return !1;
  }
}
function Ol() {
  const e = document.querySelector(".gradio-container");
  if (!e)
    return "";
  const t = e.className.match(/gradio-container-(.+)/);
  return t ? t[1] : "";
}
const jl = +Ol()[0];
function nt(e, t, n) {
  const r = jl >= 5 ? "gradio_api/" : "";
  return e == null ? n ? `/proxy=${n}${r}file=` : `${t}${r}file=` : Fl(e) ? e : n ? `/proxy=${n}${r}file=${e}` : `${t}/${r}file=${e}`;
}
const kl = (e) => !!e.url;
function To(e, t, n) {
  if (e)
    return kl(e) ? e.url : typeof e == "string" ? e.startsWith("http") ? e : nt(e, t, n) : e;
}
const Al = ({
  options: e,
  urlProxyUrl: t,
  urlRoot: n,
  onWelcomePromptSelect: r
}) => {
  var a;
  const {
    prompts: o,
    ...s
  } = e, i = ue(() => he(o || {}, {
    omitNull: !0
  }), [o]);
  return /* @__PURE__ */ S.jsxs(Ee, {
    vertical: !0,
    gap: "middle",
    children: [/* @__PURE__ */ S.jsx(ll, {
      ...s,
      icon: To(s.icon, n, t),
      styles: {
        ...s == null ? void 0 : s.styles,
        icon: {
          flexShrink: 0,
          ...(a = s == null ? void 0 : s.styles) == null ? void 0 : a.icon
        }
      },
      classNames: s.class_names,
      className: j(s.elem_classes),
      style: s.elem_style
    }), /* @__PURE__ */ S.jsx(Cn, {
      ...i,
      classNames: i == null ? void 0 : i.class_names,
      className: j(i == null ? void 0 : i.elem_classes),
      style: i == null ? void 0 : i.elem_style,
      onItemClick: ({
        data: l
      }) => {
        r({
          value: l
        });
      }
    })]
  });
}, $r = Symbol(), Rr = Symbol(), Pr = Symbol(), Ir = Symbol(), zl = (e) => e ? typeof e == "string" ? {
  src: e
} : ((n) => !!n.url)(e) ? {
  src: e.url
} : e.src ? {
  ...e,
  src: typeof e.src == "string" ? e.src : e.src.url
} : e : void 0, Dl = (e) => typeof e == "string" ? [{
  type: "text",
  content: e
}] : Array.isArray(e) ? e.map((t) => typeof t == "string" ? {
  type: "text",
  content: t
} : t) : ve(e) ? [e] : [], Hl = (e, t) => {
  if (typeof e == "string")
    return t[0];
  if (Array.isArray(e)) {
    const n = [...e];
    return Object.keys(t).forEach((r) => {
      const o = n[r];
      typeof o == "string" ? n[r] = t[r] : n[r] = {
        ...o,
        content: t[r]
      };
    }), n;
  }
  return ve(e) ? {
    ...e,
    content: t[0]
  } : e;
}, $o = (e, t, n) => typeof e == "string" ? e : Array.isArray(e) ? e.map((r) => $o(r, t, n)).filter(Boolean).join(`
`) : ve(e) ? e.copyable ?? !0 ? typeof e.content == "string" ? e.content : e.type === "file" ? JSON.stringify(e.content.map((r) => To(r, t, n))) : JSON.stringify(e.content) : "" : JSON.stringify(e), Ro = (e, t) => (e || []).map((n) => ({
  ...t(n),
  children: Array.isArray(n.children) ? Ro(n.children, t) : void 0
})), Bl = ({
  content: e,
  className: t,
  style: n,
  disabled: r,
  urlRoot: o,
  urlProxyUrl: s,
  onCopy: i
}) => {
  const a = ue(() => $o(e, o, s), [e, s, o]), l = J(null);
  return /* @__PURE__ */ S.jsx(Te.Text, {
    copyable: {
      tooltips: !1,
      onCopy() {
        i == null || i(a);
      },
      text: a,
      icon: [/* @__PURE__ */ S.jsx(se, {
        ref: l,
        variant: "text",
        color: "default",
        disabled: r,
        size: "small",
        className: t,
        style: n,
        icon: /* @__PURE__ */ S.jsx(ns, {})
      }, "copy"), /* @__PURE__ */ S.jsx(se, {
        variant: "text",
        color: "default",
        size: "small",
        disabled: r,
        className: t,
        style: n,
        icon: /* @__PURE__ */ S.jsx(Lr, {})
      }, "copied")]
    }
  });
}, Wl = ({
  action: e,
  disabledActions: t,
  message: n,
  onCopy: r,
  onDelete: o,
  onEdit: s,
  onLike: i,
  onRetry: a,
  urlRoot: l,
  urlProxyUrl: u
}) => {
  var h;
  const f = J(), d = (() => {
    var y, T;
    const {
      action: v,
      disabled: g,
      disableHandler: p
    } = ve(e) ? {
      action: e.action,
      disabled: (t == null ? void 0 : t.includes(e.action)) || !!e.disabled,
      disableHandler: !!e.popconfirm
    } : {
      action: e,
      disabled: (t == null ? void 0 : t.includes(e)) || !1,
      disableHandler: !1
    };
    switch (v) {
      case "copy":
        return /* @__PURE__ */ S.jsx(Bl, {
          disabled: g,
          content: n.content,
          onCopy: r,
          urlRoot: l,
          urlProxyUrl: u
        });
      case "like":
        return f.current = () => i(!0), /* @__PURE__ */ S.jsx(se, {
          variant: "text",
          color: ((y = n.meta) == null ? void 0 : y.feedback) === "like" ? "primary" : "default",
          disabled: g,
          size: "small",
          icon: /* @__PURE__ */ S.jsx(ts, {}),
          onClick: () => {
            !p && i(!0);
          }
        });
      case "dislike":
        return f.current = () => i(!1), /* @__PURE__ */ S.jsx(se, {
          variant: "text",
          color: ((T = n.meta) == null ? void 0 : T.feedback) === "dislike" ? "primary" : "default",
          size: "small",
          icon: /* @__PURE__ */ S.jsx(es, {}),
          disabled: g,
          onClick: () => !p && i(!1)
        });
      case "retry":
        return f.current = a, /* @__PURE__ */ S.jsx(se, {
          variant: "text",
          color: "default",
          size: "small",
          disabled: g,
          icon: /* @__PURE__ */ S.jsx(Jo, {}),
          onClick: () => !p && a()
        });
      case "edit":
        return f.current = s, /* @__PURE__ */ S.jsx(se, {
          variant: "text",
          color: "default",
          size: "small",
          disabled: g,
          icon: /* @__PURE__ */ S.jsx(Zo, {}),
          onClick: () => !p && s()
        });
      case "delete":
        return f.current = o, /* @__PURE__ */ S.jsx(se, {
          variant: "text",
          color: "default",
          size: "small",
          disabled: g,
          icon: /* @__PURE__ */ S.jsx(Qo, {}),
          onClick: () => !p && o()
        });
      default:
        return null;
    }
  })();
  if (ve(e)) {
    const v = {
      ...typeof e.popconfirm == "string" ? {
        title: e.popconfirm
      } : {
        ...e.popconfirm,
        title: (h = e.popconfirm) == null ? void 0 : h.title
      },
      onConfirm() {
        var g;
        (g = f.current) == null || g.call(f);
      }
    };
    return c.createElement(e.popconfirm ? cs : c.Fragment, e.popconfirm ? v : void 0, c.createElement(e.tooltip ? us : c.Fragment, e.tooltip ? typeof e.tooltip == "string" ? {
      title: e.tooltip
    } : e.tooltip : void 0, d));
  }
  return d;
}, Vl = ({
  isEditing: e,
  onEditCancel: t,
  onEditConfirm: n,
  onCopy: r,
  onEdit: o,
  onLike: s,
  onDelete: i,
  onRetry: a,
  editValues: l,
  message: u,
  extra: f,
  index: m,
  actions: d,
  disabledActions: h,
  urlRoot: v,
  urlProxyUrl: g
}) => e ? /* @__PURE__ */ S.jsxs(Ee, {
  justify: "end",
  children: [/* @__PURE__ */ S.jsx(se, {
    variant: "text",
    color: "default",
    size: "small",
    icon: /* @__PURE__ */ S.jsx(Yo, {}),
    onClick: () => {
      t == null || t();
    }
  }), /* @__PURE__ */ S.jsx(se, {
    variant: "text",
    color: "default",
    size: "small",
    icon: /* @__PURE__ */ S.jsx(Lr, {}),
    onClick: () => {
      const p = Hl(u.content, l);
      n == null || n({
        index: m,
        value: p,
        previous_value: u.content
      });
    }
  })]
}) : /* @__PURE__ */ S.jsx(Ee, {
  justify: "space-between",
  align: "center",
  gap: f && (d != null && d.length) ? "small" : void 0,
  children: (u.role === "user" ? ["extra", "actions"] : ["actions", "extra"]).map((p) => {
    switch (p) {
      case "extra":
        return /* @__PURE__ */ S.jsx(Te.Text, {
          type: "secondary",
          children: f
        }, "extra");
      case "actions":
        return /* @__PURE__ */ S.jsx("div", {
          children: (d || []).map((y, T) => /* @__PURE__ */ S.jsx(Wl, {
            urlRoot: v,
            urlProxyUrl: g,
            action: y,
            disabledActions: h,
            message: u,
            onCopy: (R) => r({
              value: R,
              index: m
            }),
            onDelete: () => i({
              index: m,
              value: u.content
            }),
            onEdit: () => o(m),
            onLike: (R) => s == null ? void 0 : s({
              value: u.content,
              liked: R,
              index: m
            }),
            onRetry: () => a == null ? void 0 : a({
              index: m,
              value: u.content
            })
          }, `${y}-${T}`))
        }, "actions");
    }
  })
}), Xl = ({
  markdownConfig: e,
  title: t
}) => t ? e.renderMarkdown ? /* @__PURE__ */ S.jsx(yt, {
  ...e,
  value: t
}) : /* @__PURE__ */ S.jsx(S.Fragment, {
  children: t
}) : null, Ul = ({
  item: e,
  urlRoot: t,
  urlProxyUrl: n,
  ...r
}) => {
  var i, a;
  const {
    token: o
  } = We.useToken(), s = ue(() => e ? typeof e == "string" ? {
    url: e.startsWith("http") ? e : nt(e, t, n),
    uid: e,
    name: e.split("/").pop()
  } : {
    ...e,
    uid: e.uid || e.path || e.url,
    name: e.name || e.orig_name || (e.url || e.path).split("/").pop(),
    url: e.url || nt(e.path, t, n)
  } : {}, [e, n, t]);
  return /* @__PURE__ */ S.jsx(go.FileCard, {
    ...r,
    imageProps: {
      ...r.imageProps,
      wrapperStyle: {
        width: "100%",
        height: "100%",
        ...(i = r.imageProps) == null ? void 0 : i.wrapperStyle
      },
      style: {
        width: "100%",
        height: "100%",
        objectFit: "contain",
        borderRadius: o.borderRadius,
        ...(a = r.imageProps) == null ? void 0 : a.style
      }
    },
    item: s
  });
}, Gl = ["png", "jpg", "jpeg", "gif", "bmp", "webp", "svg"];
function ql(e, t) {
  return t.some((n) => e.toLowerCase() === `.${n}`);
}
const Kl = (e, t, n) => e ? typeof e == "string" ? {
  url: e.startsWith("http") ? e : nt(e, t, n),
  uid: e,
  name: e.split("/").pop()
} : {
  ...e,
  uid: e.uid || e.path || e.url,
  name: e.name || e.orig_name || (e.url || e.path).split("/").pop(),
  url: e.url || nt(e.path, t, n)
} : {}, Yl = ({
  children: e,
  item: t
}) => {
  const {
    token: n
  } = We.useToken(), r = ue(() => {
    const o = t.name || "", s = o.match(/^(.*)\.[^.]+$/), i = s ? o.slice(s[1].length) : "";
    return ql(i, Gl);
  }, [t.name]);
  return /* @__PURE__ */ S.jsx("div", {
    className: "ms-gr-pro-chatbot-message-file-message-container",
    style: {
      borderRadius: n.borderRadius
    },
    children: r ? /* @__PURE__ */ S.jsxs(S.Fragment, {
      children: [" ", e]
    }) : /* @__PURE__ */ S.jsxs(S.Fragment, {
      children: [e, /* @__PURE__ */ S.jsx("div", {
        className: "ms-gr-pro-chatbot-message-file-message-toolbar",
        style: {
          backgroundColor: n.colorBgMask,
          zIndex: n.zIndexPopupBase,
          borderRadius: n.borderRadius
        },
        children: /* @__PURE__ */ S.jsx(se, {
          icon: /* @__PURE__ */ S.jsx(rs, {
            style: {
              color: n.colorWhite
            }
          }),
          variant: "link",
          color: "default",
          size: "small",
          href: t.url,
          target: "_blank",
          rel: "noopener noreferrer"
        })
      })]
    })
  });
}, Ql = ({
  value: e,
  urlProxyUrl: t,
  urlRoot: n,
  options: r
}) => {
  const {
    imageProps: o
  } = r;
  return /* @__PURE__ */ S.jsx(Ee, {
    gap: "small",
    wrap: !0,
    ...r,
    className: "ms-gr-pro-chatbot-message-file-message",
    children: e == null ? void 0 : e.map((s, i) => {
      const a = Kl(s, n, t);
      return /* @__PURE__ */ S.jsx(Yl, {
        item: a,
        children: /* @__PURE__ */ S.jsx(Ul, {
          item: a,
          urlRoot: n,
          urlProxyUrl: t,
          imageProps: o
        })
      }, `${a.uid}-${i}`);
    })
  });
}, Zl = ({
  value: e,
  options: t,
  onItemClick: n
}) => {
  const {
    elem_style: r,
    elem_classes: o,
    class_names: s,
    styles: i,
    ...a
  } = t;
  return /* @__PURE__ */ S.jsx(Cn, {
    ...a,
    classNames: s,
    className: j(o),
    style: r,
    styles: i,
    items: e,
    onItemClick: ({
      data: l
    }) => {
      n(l);
    }
  });
}, Mr = ({
  value: e,
  options: t
}) => {
  const {
    renderMarkdown: n,
    ...r
  } = t;
  return /* @__PURE__ */ S.jsx(S.Fragment, {
    children: n ? /* @__PURE__ */ S.jsx(yt, {
      ...r,
      value: e
    }) : e
  });
}, Jl = ({
  value: e,
  options: t
}) => {
  const {
    renderMarkdown: n,
    status: r,
    title: o,
    ...s
  } = t, [i, a] = Ze(() => r !== "done");
  return _e(() => {
    a(r !== "done");
  }, [r]), /* @__PURE__ */ S.jsx(S.Fragment, {
    children: /* @__PURE__ */ S.jsx(ds, {
      activeKey: i ? ["tool"] : [],
      onChange: () => {
        a(!i);
      },
      items: [{
        key: "tool",
        label: n ? /* @__PURE__ */ S.jsx(yt, {
          ...s,
          value: o
        }) : o,
        children: n ? /* @__PURE__ */ S.jsx(yt, {
          ...s,
          value: e
        }) : e
      }]
    })
  });
}, ec = ["text", "tool"], tc = ({
  isEditing: e,
  index: t,
  message: n,
  isLastMessage: r,
  markdownConfig: o,
  onEdit: s,
  onSuggestionSelect: i,
  urlProxyUrl: a,
  urlRoot: l
}) => {
  const u = J(null), f = () => Dl(n.content).map((d, h) => {
    const v = () => {
      var g;
      if (e && (d.editable ?? !0) && ec.includes(d.type)) {
        const p = d.content, y = (g = u.current) == null ? void 0 : g.getBoundingClientRect().width;
        return /* @__PURE__ */ S.jsx("div", {
          style: {
            width: y,
            minWidth: 200,
            maxWidth: "100%"
          },
          children: /* @__PURE__ */ S.jsx(fs.TextArea, {
            autoSize: {
              minRows: 1,
              maxRows: 10
            },
            defaultValue: p,
            onChange: (T) => {
              s(h, T.target.value);
            }
          })
        });
      }
      switch (d.type) {
        case "text":
          return /* @__PURE__ */ S.jsx(Mr, {
            value: d.content,
            options: he({
              ...o,
              ...mt(d.options)
            }, {
              omitNull: !0
            })
          });
        case "tool":
          return /* @__PURE__ */ S.jsx(Jl, {
            value: d.content,
            options: he({
              ...o,
              ...mt(d.options)
            }, {
              omitNull: !0
            })
          });
        case "file":
          return /* @__PURE__ */ S.jsx(Ql, {
            value: d.content,
            urlRoot: l,
            urlProxyUrl: a,
            options: he(d.options || {}, {
              omitNull: !0
            })
          });
        case "suggestion":
          return /* @__PURE__ */ S.jsx(Zl, {
            value: r ? d.content : Ro(d.content, (p) => ({
              ...p,
              disabled: p.disabled ?? !0
            })),
            options: he(d.options || {}, {
              omitNull: !0
            }),
            onItemClick: (p) => {
              i({
                index: t,
                value: p
              });
            }
          });
        default:
          return typeof d.content != "string" ? null : /* @__PURE__ */ S.jsx(Mr, {
            value: d.content,
            options: he({
              ...o,
              ...mt(d.options)
            }, {
              omitNull: !0
            })
          });
      }
    };
    return /* @__PURE__ */ S.jsx(c.Fragment, {
      children: v()
    }, h);
  });
  return /* @__PURE__ */ S.jsx("div", {
    ref: u,
    children: /* @__PURE__ */ S.jsx(Ee, {
      vertical: !0,
      gap: "small",
      children: f()
    })
  });
}, uc = ti(Sl(["roles"], ({
  id: e,
  className: t,
  style: n,
  height: r,
  minHeight: o,
  maxHeight: s,
  value: i,
  roles: a,
  urlRoot: l,
  urlProxyUrl: u,
  themeMode: f,
  autoScroll: m = !0,
  showScrollToBottomButton: d = !0,
  scrollToBottomButtonOffset: h = 200,
  markdownConfig: v,
  welcomeConfig: g,
  userConfig: p,
  botConfig: y,
  onValueChange: T,
  onCopy: R,
  onChange: $,
  onEdit: E,
  onRetry: x,
  onDelete: I,
  onLike: _,
  onSuggestionSelect: P,
  onWelcomePromptSelect: N
}) => {
  const z = ue(() => ({
    variant: "borderless",
    ...g ? he(g, {
      omitNull: !0
    }) : {}
  }), [g]), k = ue(() => ({
    lineBreaks: !0,
    renderMarkdown: !0,
    ...mt(v),
    urlRoot: l,
    themeMode: f
  }), [v, f, l]), w = ue(() => p ? he(p, {
    omitNull: !0
  }) : {}, [p]), b = ue(() => y ? he(y, {
    omitNull: !0
  }) : {}, [y]), M = ue(() => {
    const C = (i || []).map((K, X) => {
      const me = X === i.length - 1, ce = he(K, {
        omitNull: !0
      });
      return {
        ...An(ce, ["header", "footer", "avatar"]),
        [Co]: X,
        [$r]: ce.header,
        [Rr]: ce.footer,
        [Pr]: ce.avatar,
        [Ir]: me,
        key: ce.key ?? `${X}`
      };
    }).filter((K) => K.role !== "system");
    return C.length > 0 ? C : [{
      role: "chatbot-internal-welcome"
    }];
  }, [i]), F = J(null), [D, W] = Ze(-1), [re, te] = Ze({}), U = J(), B = oe((C, K) => {
    te((X) => ({
      ...X,
      [C]: K
    }));
  }), G = oe($);
  _e(() => {
    Ps(U.current, i) || (G(), U.current = i);
  }, [i, G]);
  const V = oe((C) => {
    P == null || P(C);
  }), q = oe((C) => {
    N == null || N(C);
  }), Se = oe((C) => {
    x == null || x(C);
  }), fe = oe((C) => {
    W(C);
  }), Ye = oe(() => {
    W(-1);
  }), Oe = oe((C) => {
    W(-1), T([...i.slice(0, C.index), {
      ...i[C.index],
      content: C.value
    }, ...i.slice(C.index + 1)]), E == null || E(C);
  }), je = oe((C) => {
    R == null || R(C);
  }), ke = oe((C) => {
    _ == null || _(C), T(Cr(i, (K) => {
      const X = K[C.index].meta || {}, me = C.liked ? "like" : "dislike";
      K[C.index] = {
        ...K[C.index],
        meta: {
          ...X,
          feedback: X.feedback === me ? null : me
        }
      };
    }));
  }), xe = oe((C) => {
    T(Cr(i, (K) => {
      K.splice(C.index, 1);
    })), I == null || I(C);
  }), Ae = Ll({
    roles: a,
    preProcess(C, K) {
      var me, ce, Z, Y, ie, Pe, Ie, Rn, Pn, In, Mn, Ln;
      const X = C.role === "user";
      return {
        ...C,
        style: C.elem_style,
        className: j(C.elem_classes, "ms-gr-pro-chatbot-message"),
        classNames: {
          ...C.class_names,
          avatar: j(X ? (me = w == null ? void 0 : w.class_names) == null ? void 0 : me.avatar : (ce = b == null ? void 0 : b.class_names) == null ? void 0 : ce.avatar, (Z = C.class_names) == null ? void 0 : Z.avatar, "ms-gr-pro-chatbot-message-avatar"),
          header: j(X ? (Y = w == null ? void 0 : w.class_names) == null ? void 0 : Y.header : (ie = b == null ? void 0 : b.class_names) == null ? void 0 : ie.header, (Pe = C.class_names) == null ? void 0 : Pe.header, "ms-gr-pro-chatbot-message-header"),
          footer: j(X ? (Ie = w == null ? void 0 : w.class_names) == null ? void 0 : Ie.footer : (Rn = b == null ? void 0 : b.class_names) == null ? void 0 : Rn.footer, (Pn = C.class_names) == null ? void 0 : Pn.footer, "ms-gr-pro-chatbot-message-footer", K === D ? "ms-gr-pro-chatbot-message-footer-editing" : void 0),
          content: j(X ? (In = w == null ? void 0 : w.class_names) == null ? void 0 : In.content : (Mn = b == null ? void 0 : b.class_names) == null ? void 0 : Mn.content, (Ln = C.class_names) == null ? void 0 : Ln.content, "ms-gr-pro-chatbot-message-content")
        }
      };
    },
    postProcess(C, K) {
      const X = C.role === "user";
      switch (C.role) {
        case "chatbot-internal-welcome":
          return {
            variant: "borderless",
            styles: {
              content: {
                width: "100%"
              }
            },
            messageRender() {
              return /* @__PURE__ */ S.jsx(Al, {
                urlRoot: l,
                urlProxyUrl: u,
                options: z || {},
                onWelcomePromptSelect: q
              });
            }
          };
        case "user":
        case "assistant":
          return {
            ...An(X ? w : b, ["actions", "avatar", "header"]),
            ...C,
            style: {
              ...X ? w == null ? void 0 : w.style : b == null ? void 0 : b.style,
              ...C.style
            },
            className: j(C.className, X ? w == null ? void 0 : w.elem_classes : b == null ? void 0 : b.elem_classes),
            header: /* @__PURE__ */ S.jsx(Xl, {
              title: C[$r] ?? (X ? w == null ? void 0 : w.header : b == null ? void 0 : b.header),
              markdownConfig: k
            }),
            avatar: zl(C[Pr] ?? (X ? w == null ? void 0 : w.avatar : b == null ? void 0 : b.avatar)),
            footer: (
              // bubbleProps[lastMessageSymbol] &&
              C.loading || C.status === "pending" ? null : /* @__PURE__ */ S.jsx(Vl, {
                isEditing: D === K,
                message: C,
                extra: C[Rr] ?? (X ? w == null ? void 0 : w.footer : b == null ? void 0 : b.footer),
                urlRoot: l,
                urlProxyUrl: u,
                editValues: re,
                index: K,
                actions: C.actions ?? (X ? (w == null ? void 0 : w.actions) || [] : (b == null ? void 0 : b.actions) || []),
                disabledActions: C.disabled_actions ?? (X ? (w == null ? void 0 : w.disabled_actions) || [] : (b == null ? void 0 : b.disabled_actions) || []),
                onEditCancel: Ye,
                onEditConfirm: Oe,
                onCopy: je,
                onEdit: fe,
                onDelete: xe,
                onRetry: Se,
                onLike: ke
              })
            ),
            messageRender() {
              return /* @__PURE__ */ S.jsx(tc, {
                index: K,
                urlProxyUrl: u,
                urlRoot: l,
                isEditing: D === K,
                message: C,
                isLastMessage: C[Ir] || !1,
                markdownConfig: k,
                onEdit: B,
                onSuggestionSelect: V
              });
            }
          };
        default:
          return;
      }
    }
  }, [D, w, z, b, k, re]), {
    scrollToBottom: ot,
    showScrollButton: Bt
  } = Nl({
    ref: F,
    value: i,
    autoScroll: m,
    scrollButtonOffset: h
  });
  return /* @__PURE__ */ S.jsxs("div", {
    id: e,
    className: j(t, "ms-gr-pro-chatbot"),
    style: {
      height: r,
      minHeight: o,
      maxHeight: s,
      ...n
    },
    children: [/* @__PURE__ */ S.jsx(En.List, {
      ref: F,
      className: "ms-gr-pro-chatbot-messages",
      autoScroll: !1,
      roles: Ae,
      items: M
    }), d && Bt && /* @__PURE__ */ S.jsx("div", {
      className: "ms-gr-pro-chatbot-scroll-to-bottom-button",
      children: /* @__PURE__ */ S.jsx(se, {
        icon: /* @__PURE__ */ S.jsx(os, {}),
        shape: "circle",
        variant: "outlined",
        color: "primary",
        onClick: () => ot("smooth")
      })
    })]
  });
}));
export {
  uc as Chatbot,
  uc as default
};
