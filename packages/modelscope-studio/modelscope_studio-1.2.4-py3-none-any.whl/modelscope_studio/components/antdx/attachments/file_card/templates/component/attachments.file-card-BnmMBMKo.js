var Nt = (e) => {
  throw TypeError(e);
};
var zt = (e, t, r) => t.has(e) || Nt("Cannot " + r);
var de = (e, t, r) => (zt(e, t, "read from private field"), r ? r.call(e) : t.get(e)), Ht = (e, t, r) => t.has(e) ? Nt("Cannot add the same private member more than once") : t instanceof WeakSet ? t.add(e) : t.set(e, r), Bt = (e, t, r, n) => (zt(e, t, "write to private field"), n ? n.call(e, r) : t.set(e, r), r);
import { i as gn, a as St, r as hn, w as De, g as vn, b as bn, c as Q } from "./Index-uWjqb108.js";
const M = window.ms_globals.React, l = window.ms_globals.React, un = window.ms_globals.React.forwardRef, se = window.ms_globals.React.useRef, fn = window.ms_globals.React.useState, xe = window.ms_globals.React.useEffect, Tr = window.ms_globals.React.useMemo, dn = window.ms_globals.React.version, pn = window.ms_globals.React.isValidElement, mn = window.ms_globals.React.useLayoutEffect, Vt = window.ms_globals.ReactDOM, He = window.ms_globals.ReactDOM.createPortal, yn = window.ms_globals.internalContext.useContextPropsContext, Sn = window.ms_globals.internalContext.ContextPropsProvider, xn = window.ms_globals.antd.ConfigProvider, Lr = window.ms_globals.antd.Upload, Ee = window.ms_globals.antd.theme, wn = window.ms_globals.antd.Progress, En = window.ms_globals.antd.Image, at = window.ms_globals.antd.Button, Cn = window.ms_globals.antd.Flex, lt = window.ms_globals.antd.Typography, _n = window.ms_globals.antdIcons.FileTextFilled, Rn = window.ms_globals.antdIcons.CloseCircleFilled, Tn = window.ms_globals.antdIcons.FileExcelFilled, Ln = window.ms_globals.antdIcons.FileImageFilled, Pn = window.ms_globals.antdIcons.FileMarkdownFilled, Mn = window.ms_globals.antdIcons.FilePdfFilled, In = window.ms_globals.antdIcons.FilePptFilled, On = window.ms_globals.antdIcons.FileWordFilled, $n = window.ms_globals.antdIcons.FileZipFilled, An = window.ms_globals.antdIcons.PlusOutlined, Fn = window.ms_globals.antdIcons.LeftOutlined, kn = window.ms_globals.antdIcons.RightOutlined, Ut = window.ms_globals.antdCssinjs.unit, ct = window.ms_globals.antdCssinjs.token2CSSVar, Xt = window.ms_globals.antdCssinjs.useStyleRegister, jn = window.ms_globals.antdCssinjs.useCSSVarRegister, Dn = window.ms_globals.antdCssinjs.createTheme, Nn = window.ms_globals.antdCssinjs.useCacheToken;
var zn = /\s/;
function Hn(e) {
  for (var t = e.length; t-- && zn.test(e.charAt(t)); )
    ;
  return t;
}
var Bn = /^\s+/;
function Vn(e) {
  return e && e.slice(0, Hn(e) + 1).replace(Bn, "");
}
var Wt = NaN, Un = /^[-+]0x[0-9a-f]+$/i, Xn = /^0b[01]+$/i, Wn = /^0o[0-7]+$/i, Gn = parseInt;
function Gt(e) {
  if (typeof e == "number")
    return e;
  if (gn(e))
    return Wt;
  if (St(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = St(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = Vn(e);
  var r = Xn.test(e);
  return r || Wn.test(e) ? Gn(e.slice(2), r ? 2 : 8) : Un.test(e) ? Wt : +e;
}
var ut = function() {
  return hn.Date.now();
}, qn = "Expected a function", Kn = Math.max, Zn = Math.min;
function Qn(e, t, r) {
  var n, o, i, s, a, c, u = 0, p = !1, f = !1, d = !0;
  if (typeof e != "function")
    throw new TypeError(qn);
  t = Gt(t) || 0, St(r) && (p = !!r.leading, f = "maxWait" in r, i = f ? Kn(Gt(r.maxWait) || 0, t) : i, d = "trailing" in r ? !!r.trailing : d);
  function m(v) {
    var _ = n, y = o;
    return n = o = void 0, u = v, s = e.apply(y, _), s;
  }
  function b(v) {
    return u = v, a = setTimeout(h, t), p ? m(v) : s;
  }
  function x(v) {
    var _ = v - c, y = v - u, L = t - _;
    return f ? Zn(L, i - y) : L;
  }
  function g(v) {
    var _ = v - c, y = v - u;
    return c === void 0 || _ >= t || _ < 0 || f && y >= i;
  }
  function h() {
    var v = ut();
    if (g(v))
      return E(v);
    a = setTimeout(h, x(v));
  }
  function E(v) {
    return a = void 0, d && n ? m(v) : (n = o = void 0, s);
  }
  function T() {
    a !== void 0 && clearTimeout(a), u = 0, n = c = o = a = void 0;
  }
  function S() {
    return a === void 0 ? s : E(ut());
  }
  function w() {
    var v = ut(), _ = g(v);
    if (n = arguments, o = this, c = v, _) {
      if (a === void 0)
        return b(c);
      if (f)
        return clearTimeout(a), a = setTimeout(h, t), m(c);
    }
    return a === void 0 && (a = setTimeout(h, t)), s;
  }
  return w.cancel = T, w.flush = S, w;
}
var Pr = {
  exports: {}
}, Ue = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Yn = l, Jn = Symbol.for("react.element"), eo = Symbol.for("react.fragment"), to = Object.prototype.hasOwnProperty, ro = Yn.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, no = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Mr(e, t, r) {
  var n, o = {}, i = null, s = null;
  r !== void 0 && (i = "" + r), t.key !== void 0 && (i = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (n in t) to.call(t, n) && !no.hasOwnProperty(n) && (o[n] = t[n]);
  if (e && e.defaultProps) for (n in t = e.defaultProps, t) o[n] === void 0 && (o[n] = t[n]);
  return {
    $$typeof: Jn,
    type: e,
    key: i,
    ref: s,
    props: o,
    _owner: ro.current
  };
}
Ue.Fragment = eo;
Ue.jsx = Mr;
Ue.jsxs = Mr;
Pr.exports = Ue;
var X = Pr.exports;
const {
  SvelteComponent: oo,
  assign: qt,
  binding_callbacks: Kt,
  check_outros: io,
  children: Ir,
  claim_element: Or,
  claim_space: so,
  component_subscribe: Zt,
  compute_slots: ao,
  create_slot: lo,
  detach: pe,
  element: $r,
  empty: Qt,
  exclude_internal_props: Yt,
  get_all_dirty_from_scope: co,
  get_slot_changes: uo,
  group_outros: fo,
  init: po,
  insert_hydration: Ne,
  safe_not_equal: mo,
  set_custom_element_data: Ar,
  space: go,
  transition_in: ze,
  transition_out: xt,
  update_slot_base: ho
} = window.__gradio__svelte__internal, {
  beforeUpdate: vo,
  getContext: bo,
  onDestroy: yo,
  setContext: So
} = window.__gradio__svelte__internal;
function Jt(e) {
  let t, r;
  const n = (
    /*#slots*/
    e[7].default
  ), o = lo(
    n,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = $r("svelte-slot"), o && o.c(), this.h();
    },
    l(i) {
      t = Or(i, "SVELTE-SLOT", {
        class: !0
      });
      var s = Ir(t);
      o && o.l(s), s.forEach(pe), this.h();
    },
    h() {
      Ar(t, "class", "svelte-1rt0kpf");
    },
    m(i, s) {
      Ne(i, t, s), o && o.m(t, null), e[9](t), r = !0;
    },
    p(i, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && ho(
        o,
        n,
        i,
        /*$$scope*/
        i[6],
        r ? uo(
          n,
          /*$$scope*/
          i[6],
          s,
          null
        ) : co(
          /*$$scope*/
          i[6]
        ),
        null
      );
    },
    i(i) {
      r || (ze(o, i), r = !0);
    },
    o(i) {
      xt(o, i), r = !1;
    },
    d(i) {
      i && pe(t), o && o.d(i), e[9](null);
    }
  };
}
function xo(e) {
  let t, r, n, o, i = (
    /*$$slots*/
    e[4].default && Jt(e)
  );
  return {
    c() {
      t = $r("react-portal-target"), r = go(), i && i.c(), n = Qt(), this.h();
    },
    l(s) {
      t = Or(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), Ir(t).forEach(pe), r = so(s), i && i.l(s), n = Qt(), this.h();
    },
    h() {
      Ar(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      Ne(s, t, a), e[8](t), Ne(s, r, a), i && i.m(s, a), Ne(s, n, a), o = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? i ? (i.p(s, a), a & /*$$slots*/
      16 && ze(i, 1)) : (i = Jt(s), i.c(), ze(i, 1), i.m(n.parentNode, n)) : i && (fo(), xt(i, 1, 1, () => {
        i = null;
      }), io());
    },
    i(s) {
      o || (ze(i), o = !0);
    },
    o(s) {
      xt(i), o = !1;
    },
    d(s) {
      s && (pe(t), pe(r), pe(n)), e[8](null), i && i.d(s);
    }
  };
}
function er(e) {
  const {
    svelteInit: t,
    ...r
  } = e;
  return r;
}
function wo(e, t, r) {
  let n, o, {
    $$slots: i = {},
    $$scope: s
  } = t;
  const a = ao(i);
  let {
    svelteInit: c
  } = t;
  const u = De(er(t)), p = De();
  Zt(e, p, (S) => r(0, n = S));
  const f = De();
  Zt(e, f, (S) => r(1, o = S));
  const d = [], m = bo("$$ms-gr-react-wrapper"), {
    slotKey: b,
    slotIndex: x,
    subSlotIndex: g
  } = vn() || {}, h = c({
    parent: m,
    props: u,
    target: p,
    slot: f,
    slotKey: b,
    slotIndex: x,
    subSlotIndex: g,
    onDestroy(S) {
      d.push(S);
    }
  });
  So("$$ms-gr-react-wrapper", h), vo(() => {
    u.set(er(t));
  }), yo(() => {
    d.forEach((S) => S());
  });
  function E(S) {
    Kt[S ? "unshift" : "push"](() => {
      n = S, p.set(n);
    });
  }
  function T(S) {
    Kt[S ? "unshift" : "push"](() => {
      o = S, f.set(o);
    });
  }
  return e.$$set = (S) => {
    r(17, t = qt(qt({}, t), Yt(S))), "svelteInit" in S && r(5, c = S.svelteInit), "$$scope" in S && r(6, s = S.$$scope);
  }, t = Yt(t), [n, o, p, f, a, c, s, i, E, T];
}
class Eo extends oo {
  constructor(t) {
    super(), po(this, t, wo, xo, mo, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: ys
} = window.__gradio__svelte__internal, tr = window.ms_globals.rerender, ft = window.ms_globals.tree;
function Co(e, t = {}) {
  function r(n) {
    const o = De(), i = new Eo({
      ...n,
      props: {
        svelteInit(s) {
          window.ms_globals.autokey += 1;
          const a = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: e,
            props: s.props,
            slot: s.slot,
            target: s.target,
            slotIndex: s.slotIndex,
            subSlotIndex: s.subSlotIndex,
            ignore: t.ignore,
            slotKey: s.slotKey,
            nodes: []
          }, c = s.parent ?? ft;
          return c.nodes = [...c.nodes, a], tr({
            createPortal: He,
            node: ft
          }), s.onDestroy(() => {
            c.nodes = c.nodes.filter((u) => u.svelteInstance !== o), tr({
              createPortal: He,
              node: ft
            });
          }), a;
        },
        ...n.props
      }
    });
    return o.set(i), i;
  }
  return new Promise((n) => {
    window.ms_globals.initializePromise.then(() => {
      n(r);
    });
  });
}
const _o = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ro(e) {
  return e ? Object.keys(e).reduce((t, r) => {
    const n = e[r];
    return t[r] = To(r, n), t;
  }, {}) : {};
}
function To(e, t) {
  return typeof t == "number" && !_o.includes(e) ? t + "px" : t;
}
function wt(e) {
  const t = [], r = e.cloneNode(!1);
  if (e._reactElement) {
    const o = l.Children.toArray(e._reactElement.props.children).map((i) => {
      if (l.isValidElement(i) && i.props.__slot__) {
        const {
          portals: s,
          clonedElement: a
        } = wt(i.props.el);
        return l.cloneElement(i, {
          ...i.props,
          el: a,
          children: [...l.Children.toArray(i.props.children), ...s]
        });
      }
      return null;
    });
    return o.originalChildren = e._reactElement.props.children, t.push(He(l.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: o
    }), r)), {
      clonedElement: r,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: s,
      type: a,
      useCapture: c
    }) => {
      r.addEventListener(a, s, c);
    });
  });
  const n = Array.from(e.childNodes);
  for (let o = 0; o < n.length; o++) {
    const i = n[o];
    if (i.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = wt(i);
      t.push(...a), r.appendChild(s);
    } else i.nodeType === 3 && r.appendChild(i.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Lo(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const we = un(({
  slot: e,
  clone: t,
  className: r,
  style: n,
  observeAttributes: o
}, i) => {
  const s = se(), [a, c] = fn([]), {
    forceClone: u
  } = yn(), p = u ? !0 : t;
  return xe(() => {
    var x;
    if (!s.current || !e)
      return;
    let f = e;
    function d() {
      let g = f;
      if (f.tagName.toLowerCase() === "svelte-slot" && f.children.length === 1 && f.children[0] && (g = f.children[0], g.tagName.toLowerCase() === "react-portal-target" && g.children[0] && (g = g.children[0])), Lo(i, g), r && g.classList.add(...r.split(" ")), n) {
        const h = Ro(n);
        Object.keys(h).forEach((E) => {
          g.style[E] = h[E];
        });
      }
    }
    let m = null, b = null;
    if (p && window.MutationObserver) {
      let g = function() {
        var S, w, v;
        (S = s.current) != null && S.contains(f) && ((w = s.current) == null || w.removeChild(f));
        const {
          portals: E,
          clonedElement: T
        } = wt(e);
        f = T, c(E), f.style.display = "contents", b && clearTimeout(b), b = setTimeout(() => {
          d();
        }, 50), (v = s.current) == null || v.appendChild(f);
      };
      g();
      const h = Qn(() => {
        g(), m == null || m.disconnect(), m == null || m.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: o
        });
      }, 50);
      m = new window.MutationObserver(h), m.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      f.style.display = "contents", d(), (x = s.current) == null || x.appendChild(f);
    return () => {
      var g, h;
      f.style.display = "", (g = s.current) != null && g.contains(f) && ((h = s.current) == null || h.removeChild(f)), m == null || m.disconnect();
    };
  }, [e, p, r, n, i, o, u]), l.createElement("react-child", {
    ref: s,
    style: {
      display: "contents"
    }
  }, ...a);
});
function Po(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function Mo(e, t = !1) {
  try {
    if (bn(e))
      return e;
    if (t && !Po(e))
      return;
    if (typeof e == "string") {
      let r = e.trim();
      return r.startsWith(";") && (r = r.slice(1)), r.endsWith(";") && (r = r.slice(0, -1)), new Function(`return (...args) => (${r})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function dt(e, t) {
  return Tr(() => Mo(e, t), [e, t]);
}
function Io(e, t) {
  return Object.keys(e).reduce((r, n) => (e[n] !== void 0 && (r[n] = e[n]), r), {});
}
const Oo = ({
  children: e,
  ...t
}) => /* @__PURE__ */ X.jsx(X.Fragment, {
  children: e(t)
});
function $o(e) {
  return l.createElement(Oo, {
    children: e
  });
}
function rr(e, t) {
  return e ? t != null && t.forceClone || t != null && t.params ? $o((r) => /* @__PURE__ */ X.jsx(Sn, {
    forceClone: t == null ? void 0 : t.forceClone,
    params: t == null ? void 0 : t.params,
    children: /* @__PURE__ */ X.jsx(we, {
      slot: e,
      clone: t == null ? void 0 : t.clone,
      ...r
    })
  })) : /* @__PURE__ */ X.jsx(we, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function nr({
  key: e,
  slots: t,
  targets: r
}, n) {
  return t[e] ? (...o) => r ? r.map((i, s) => /* @__PURE__ */ X.jsx(l.Fragment, {
    children: rr(i, {
      clone: !0,
      params: o,
      forceClone: !0
    })
  }, s)) : /* @__PURE__ */ X.jsx(X.Fragment, {
    children: rr(t[e], {
      clone: !0,
      params: o,
      forceClone: !0
    })
  }) : void 0;
}
const Ao = "1.1.0", Fo = /* @__PURE__ */ l.createContext({}), ko = {
  classNames: {},
  styles: {},
  className: "",
  style: {}
}, jo = (e) => {
  const t = l.useContext(Fo);
  return l.useMemo(() => ({
    ...ko,
    ...t[e]
  }), [t[e]]);
};
function he() {
  return he = Object.assign ? Object.assign.bind() : function(e) {
    for (var t = 1; t < arguments.length; t++) {
      var r = arguments[t];
      for (var n in r) ({}).hasOwnProperty.call(r, n) && (e[n] = r[n]);
    }
    return e;
  }, he.apply(null, arguments);
}
function Be() {
  const {
    getPrefixCls: e,
    direction: t,
    csp: r,
    iconPrefixCls: n,
    theme: o
  } = l.useContext(xn.ConfigContext);
  return {
    theme: o,
    getPrefixCls: e,
    direction: t,
    csp: r,
    iconPrefixCls: n
  };
}
function ve(e) {
  var t = M.useRef();
  t.current = e;
  var r = M.useCallback(function() {
    for (var n, o = arguments.length, i = new Array(o), s = 0; s < o; s++)
      i[s] = arguments[s];
    return (n = t.current) === null || n === void 0 ? void 0 : n.call.apply(n, [t].concat(i));
  }, []);
  return r;
}
function Do(e) {
  if (Array.isArray(e)) return e;
}
function No(e, t) {
  var r = e == null ? null : typeof Symbol < "u" && e[Symbol.iterator] || e["@@iterator"];
  if (r != null) {
    var n, o, i, s, a = [], c = !0, u = !1;
    try {
      if (i = (r = r.call(e)).next, t === 0) {
        if (Object(r) !== r) return;
        c = !1;
      } else for (; !(c = (n = i.call(r)).done) && (a.push(n.value), a.length !== t); c = !0) ;
    } catch (p) {
      u = !0, o = p;
    } finally {
      try {
        if (!c && r.return != null && (s = r.return(), Object(s) !== s)) return;
      } finally {
        if (u) throw o;
      }
    }
    return a;
  }
}
function or(e, t) {
  (t == null || t > e.length) && (t = e.length);
  for (var r = 0, n = Array(t); r < t; r++) n[r] = e[r];
  return n;
}
function zo(e, t) {
  if (e) {
    if (typeof e == "string") return or(e, t);
    var r = {}.toString.call(e).slice(8, -1);
    return r === "Object" && e.constructor && (r = e.constructor.name), r === "Map" || r === "Set" ? Array.from(e) : r === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r) ? or(e, t) : void 0;
  }
}
function Ho() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function W(e, t) {
  return Do(e) || No(e, t) || zo(e, t) || Ho();
}
function Xe() {
  return !!(typeof window < "u" && window.document && window.document.createElement);
}
var ir = Xe() ? M.useLayoutEffect : M.useEffect, Bo = function(t, r) {
  var n = M.useRef(!0);
  ir(function() {
    return t(n.current);
  }, r), ir(function() {
    return n.current = !1, function() {
      n.current = !0;
    };
  }, []);
}, sr = function(t, r) {
  Bo(function(n) {
    if (!n)
      return t();
  }, r);
};
function Ce(e) {
  var t = M.useRef(!1), r = M.useState(e), n = W(r, 2), o = n[0], i = n[1];
  M.useEffect(function() {
    return t.current = !1, function() {
      t.current = !0;
    };
  }, []);
  function s(a, c) {
    c && t.current || i(a);
  }
  return [o, s];
}
function pt(e) {
  return e !== void 0;
}
function Vo(e, t) {
  var r = t || {}, n = r.defaultValue, o = r.value, i = r.onChange, s = r.postState, a = Ce(function() {
    return pt(o) ? o : pt(n) ? typeof n == "function" ? n() : n : typeof e == "function" ? e() : e;
  }), c = W(a, 2), u = c[0], p = c[1], f = o !== void 0 ? o : u, d = s ? s(f) : f, m = ve(i), b = Ce([f]), x = W(b, 2), g = x[0], h = x[1];
  sr(function() {
    var T = g[0];
    u !== T && m(u, T);
  }, [g]), sr(function() {
    pt(o) || p(o);
  }, [o]);
  var E = ve(function(T, S) {
    p(T, S), h([f], S);
  });
  return [d, E];
}
function B(e) {
  "@babel/helpers - typeof";
  return B = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, B(e);
}
var Fr = {
  exports: {}
}, I = {};
/**
 * @license React
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Ot = Symbol.for("react.element"), $t = Symbol.for("react.portal"), We = Symbol.for("react.fragment"), Ge = Symbol.for("react.strict_mode"), qe = Symbol.for("react.profiler"), Ke = Symbol.for("react.provider"), Ze = Symbol.for("react.context"), Uo = Symbol.for("react.server_context"), Qe = Symbol.for("react.forward_ref"), Ye = Symbol.for("react.suspense"), Je = Symbol.for("react.suspense_list"), et = Symbol.for("react.memo"), tt = Symbol.for("react.lazy"), Xo = Symbol.for("react.offscreen"), kr;
kr = Symbol.for("react.module.reference");
function Y(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case Ot:
        switch (e = e.type, e) {
          case We:
          case qe:
          case Ge:
          case Ye:
          case Je:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case Uo:
              case Ze:
              case Qe:
              case tt:
              case et:
              case Ke:
                return e;
              default:
                return t;
            }
        }
      case $t:
        return t;
    }
  }
}
I.ContextConsumer = Ze;
I.ContextProvider = Ke;
I.Element = Ot;
I.ForwardRef = Qe;
I.Fragment = We;
I.Lazy = tt;
I.Memo = et;
I.Portal = $t;
I.Profiler = qe;
I.StrictMode = Ge;
I.Suspense = Ye;
I.SuspenseList = Je;
I.isAsyncMode = function() {
  return !1;
};
I.isConcurrentMode = function() {
  return !1;
};
I.isContextConsumer = function(e) {
  return Y(e) === Ze;
};
I.isContextProvider = function(e) {
  return Y(e) === Ke;
};
I.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === Ot;
};
I.isForwardRef = function(e) {
  return Y(e) === Qe;
};
I.isFragment = function(e) {
  return Y(e) === We;
};
I.isLazy = function(e) {
  return Y(e) === tt;
};
I.isMemo = function(e) {
  return Y(e) === et;
};
I.isPortal = function(e) {
  return Y(e) === $t;
};
I.isProfiler = function(e) {
  return Y(e) === qe;
};
I.isStrictMode = function(e) {
  return Y(e) === Ge;
};
I.isSuspense = function(e) {
  return Y(e) === Ye;
};
I.isSuspenseList = function(e) {
  return Y(e) === Je;
};
I.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === We || e === qe || e === Ge || e === Ye || e === Je || e === Xo || typeof e == "object" && e !== null && (e.$$typeof === tt || e.$$typeof === et || e.$$typeof === Ke || e.$$typeof === Ze || e.$$typeof === Qe || e.$$typeof === kr || e.getModuleId !== void 0);
};
I.typeOf = Y;
Fr.exports = I;
var mt = Fr.exports, Wo = Symbol.for("react.element"), Go = Symbol.for("react.transitional.element"), qo = Symbol.for("react.fragment");
function Ko(e) {
  return (
    // Base object type
    e && B(e) === "object" && // React Element type
    (e.$$typeof === Wo || e.$$typeof === Go) && // React Fragment type
    e.type === qo
  );
}
var Zo = Number(dn.split(".")[0]), Qo = function(t, r) {
  typeof t == "function" ? t(r) : B(t) === "object" && t && "current" in t && (t.current = r);
}, Yo = function(t) {
  var r, n;
  if (!t)
    return !1;
  if (jr(t) && Zo >= 19)
    return !0;
  var o = mt.isMemo(t) ? t.type.type : t.type;
  return !(typeof o == "function" && !((r = o.prototype) !== null && r !== void 0 && r.render) && o.$$typeof !== mt.ForwardRef || typeof t == "function" && !((n = t.prototype) !== null && n !== void 0 && n.render) && t.$$typeof !== mt.ForwardRef);
};
function jr(e) {
  return /* @__PURE__ */ pn(e) && !Ko(e);
}
var Jo = function(t) {
  if (t && jr(t)) {
    var r = t;
    return r.props.propertyIsEnumerable("ref") ? r.props.ref : r.ref;
  }
  return null;
};
function ei(e, t) {
  if (B(e) != "object" || !e) return e;
  var r = e[Symbol.toPrimitive];
  if (r !== void 0) {
    var n = r.call(e, t);
    if (B(n) != "object") return n;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (t === "string" ? String : Number)(e);
}
function Dr(e) {
  var t = ei(e, "string");
  return B(t) == "symbol" ? t : t + "";
}
function R(e, t, r) {
  return (t = Dr(t)) in e ? Object.defineProperty(e, t, {
    value: r,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : e[t] = r, e;
}
function ar(e, t) {
  var r = Object.keys(e);
  if (Object.getOwnPropertySymbols) {
    var n = Object.getOwnPropertySymbols(e);
    t && (n = n.filter(function(o) {
      return Object.getOwnPropertyDescriptor(e, o).enumerable;
    })), r.push.apply(r, n);
  }
  return r;
}
function C(e) {
  for (var t = 1; t < arguments.length; t++) {
    var r = arguments[t] != null ? arguments[t] : {};
    t % 2 ? ar(Object(r), !0).forEach(function(n) {
      R(e, n, r[n]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(r)) : ar(Object(r)).forEach(function(n) {
      Object.defineProperty(e, n, Object.getOwnPropertyDescriptor(r, n));
    });
  }
  return e;
}
const _e = /* @__PURE__ */ l.createContext(null);
function lr(e) {
  const {
    getDropContainer: t,
    className: r,
    prefixCls: n,
    children: o
  } = e, {
    disabled: i
  } = l.useContext(_e), [s, a] = l.useState(), [c, u] = l.useState(null);
  if (l.useEffect(() => {
    const d = t == null ? void 0 : t();
    s !== d && a(d);
  }, [t]), l.useEffect(() => {
    if (s) {
      const d = () => {
        u(!0);
      }, m = (g) => {
        g.preventDefault();
      }, b = (g) => {
        g.relatedTarget || u(!1);
      }, x = (g) => {
        u(!1), g.preventDefault();
      };
      return document.addEventListener("dragenter", d), document.addEventListener("dragover", m), document.addEventListener("dragleave", b), document.addEventListener("drop", x), () => {
        document.removeEventListener("dragenter", d), document.removeEventListener("dragover", m), document.removeEventListener("dragleave", b), document.removeEventListener("drop", x);
      };
    }
  }, [!!s]), !(t && s && !i))
    return null;
  const f = `${n}-drop-area`;
  return /* @__PURE__ */ He(/* @__PURE__ */ l.createElement("div", {
    className: Q(f, r, {
      [`${f}-on-body`]: s.tagName === "BODY"
    }),
    style: {
      display: c ? "block" : "none"
    }
  }, o), s);
}
function cr(e) {
  return e instanceof HTMLElement || e instanceof SVGElement;
}
function ti(e) {
  return e && B(e) === "object" && cr(e.nativeElement) ? e.nativeElement : cr(e) ? e : null;
}
function ri(e) {
  var t = ti(e);
  if (t)
    return t;
  if (e instanceof l.Component) {
    var r;
    return (r = Vt.findDOMNode) === null || r === void 0 ? void 0 : r.call(Vt, e);
  }
  return null;
}
function ni(e, t) {
  if (e == null) return {};
  var r = {};
  for (var n in e) if ({}.hasOwnProperty.call(e, n)) {
    if (t.indexOf(n) !== -1) continue;
    r[n] = e[n];
  }
  return r;
}
function ur(e, t) {
  if (e == null) return {};
  var r, n, o = ni(e, t);
  if (Object.getOwnPropertySymbols) {
    var i = Object.getOwnPropertySymbols(e);
    for (n = 0; n < i.length; n++) r = i[n], t.indexOf(r) === -1 && {}.propertyIsEnumerable.call(e, r) && (o[r] = e[r]);
  }
  return o;
}
var oi = /* @__PURE__ */ M.createContext({});
function be(e, t) {
  if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function");
}
function fr(e, t) {
  for (var r = 0; r < t.length; r++) {
    var n = t[r];
    n.enumerable = n.enumerable || !1, n.configurable = !0, "value" in n && (n.writable = !0), Object.defineProperty(e, Dr(n.key), n);
  }
}
function ye(e, t, r) {
  return t && fr(e.prototype, t), r && fr(e, r), Object.defineProperty(e, "prototype", {
    writable: !1
  }), e;
}
function Et(e, t) {
  return Et = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(r, n) {
    return r.__proto__ = n, r;
  }, Et(e, t);
}
function rt(e, t) {
  if (typeof t != "function" && t !== null) throw new TypeError("Super expression must either be null or a function");
  e.prototype = Object.create(t && t.prototype, {
    constructor: {
      value: e,
      writable: !0,
      configurable: !0
    }
  }), Object.defineProperty(e, "prototype", {
    writable: !1
  }), t && Et(e, t);
}
function Ve(e) {
  return Ve = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function(t) {
    return t.__proto__ || Object.getPrototypeOf(t);
  }, Ve(e);
}
function Nr() {
  try {
    var e = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {
    }));
  } catch {
  }
  return (Nr = function() {
    return !!e;
  })();
}
function ue(e) {
  if (e === void 0) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return e;
}
function ii(e, t) {
  if (t && (B(t) == "object" || typeof t == "function")) return t;
  if (t !== void 0) throw new TypeError("Derived constructors may only return object or undefined");
  return ue(e);
}
function nt(e) {
  var t = Nr();
  return function() {
    var r, n = Ve(e);
    if (t) {
      var o = Ve(this).constructor;
      r = Reflect.construct(n, arguments, o);
    } else r = n.apply(this, arguments);
    return ii(this, r);
  };
}
var si = /* @__PURE__ */ function(e) {
  rt(r, e);
  var t = nt(r);
  function r() {
    return be(this, r), t.apply(this, arguments);
  }
  return ye(r, [{
    key: "render",
    value: function() {
      return this.props.children;
    }
  }]), r;
}(M.Component);
function ai(e) {
  var t = M.useReducer(function(a) {
    return a + 1;
  }, 0), r = W(t, 2), n = r[1], o = M.useRef(e), i = ve(function() {
    return o.current;
  }), s = ve(function(a) {
    o.current = typeof a == "function" ? a(o.current) : a, n();
  });
  return [i, s];
}
var ie = "none", Oe = "appear", $e = "enter", Ae = "leave", dr = "none", J = "prepare", me = "start", ge = "active", At = "end", zr = "prepared";
function pr(e, t) {
  var r = {};
  return r[e.toLowerCase()] = t.toLowerCase(), r["Webkit".concat(e)] = "webkit".concat(t), r["Moz".concat(e)] = "moz".concat(t), r["ms".concat(e)] = "MS".concat(t), r["O".concat(e)] = "o".concat(t.toLowerCase()), r;
}
function li(e, t) {
  var r = {
    animationend: pr("Animation", "AnimationEnd"),
    transitionend: pr("Transition", "TransitionEnd")
  };
  return e && ("AnimationEvent" in t || delete r.animationend.animation, "TransitionEvent" in t || delete r.transitionend.transition), r;
}
var ci = li(Xe(), typeof window < "u" ? window : {}), Hr = {};
if (Xe()) {
  var ui = document.createElement("div");
  Hr = ui.style;
}
var Fe = {};
function Br(e) {
  if (Fe[e])
    return Fe[e];
  var t = ci[e];
  if (t)
    for (var r = Object.keys(t), n = r.length, o = 0; o < n; o += 1) {
      var i = r[o];
      if (Object.prototype.hasOwnProperty.call(t, i) && i in Hr)
        return Fe[e] = t[i], Fe[e];
    }
  return "";
}
var Vr = Br("animationend"), Ur = Br("transitionend"), Xr = !!(Vr && Ur), mr = Vr || "animationend", gr = Ur || "transitionend";
function hr(e, t) {
  if (!e) return null;
  if (B(e) === "object") {
    var r = t.replace(/-\w/g, function(n) {
      return n[1].toUpperCase();
    });
    return e[r];
  }
  return "".concat(e, "-").concat(t);
}
const fi = function(e) {
  var t = se();
  function r(o) {
    o && (o.removeEventListener(gr, e), o.removeEventListener(mr, e));
  }
  function n(o) {
    t.current && t.current !== o && r(t.current), o && o !== t.current && (o.addEventListener(gr, e), o.addEventListener(mr, e), t.current = o);
  }
  return M.useEffect(function() {
    return function() {
      r(t.current);
    };
  }, []), [n, r];
};
var Wr = Xe() ? mn : xe, Gr = function(t) {
  return +setTimeout(t, 16);
}, qr = function(t) {
  return clearTimeout(t);
};
typeof window < "u" && "requestAnimationFrame" in window && (Gr = function(t) {
  return window.requestAnimationFrame(t);
}, qr = function(t) {
  return window.cancelAnimationFrame(t);
});
var vr = 0, Ft = /* @__PURE__ */ new Map();
function Kr(e) {
  Ft.delete(e);
}
var Ct = function(t) {
  var r = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 1;
  vr += 1;
  var n = vr;
  function o(i) {
    if (i === 0)
      Kr(n), t();
    else {
      var s = Gr(function() {
        o(i - 1);
      });
      Ft.set(n, s);
    }
  }
  return o(r), n;
};
Ct.cancel = function(e) {
  var t = Ft.get(e);
  return Kr(e), qr(t);
};
const di = function() {
  var e = M.useRef(null);
  function t() {
    Ct.cancel(e.current);
  }
  function r(n) {
    var o = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 2;
    t();
    var i = Ct(function() {
      o <= 1 ? n({
        isCanceled: function() {
          return i !== e.current;
        }
      }) : r(n, o - 1);
    });
    e.current = i;
  }
  return M.useEffect(function() {
    return function() {
      t();
    };
  }, []), [r, t];
};
var pi = [J, me, ge, At], mi = [J, zr], Zr = !1, gi = !0;
function Qr(e) {
  return e === ge || e === At;
}
const hi = function(e, t, r) {
  var n = Ce(dr), o = W(n, 2), i = o[0], s = o[1], a = di(), c = W(a, 2), u = c[0], p = c[1];
  function f() {
    s(J, !0);
  }
  var d = t ? mi : pi;
  return Wr(function() {
    if (i !== dr && i !== At) {
      var m = d.indexOf(i), b = d[m + 1], x = r(i);
      x === Zr ? s(b, !0) : b && u(function(g) {
        function h() {
          g.isCanceled() || s(b, !0);
        }
        x === !0 ? h() : Promise.resolve(x).then(h);
      });
    }
  }, [e, i]), M.useEffect(function() {
    return function() {
      p();
    };
  }, []), [f, i];
};
function vi(e, t, r, n) {
  var o = n.motionEnter, i = o === void 0 ? !0 : o, s = n.motionAppear, a = s === void 0 ? !0 : s, c = n.motionLeave, u = c === void 0 ? !0 : c, p = n.motionDeadline, f = n.motionLeaveImmediately, d = n.onAppearPrepare, m = n.onEnterPrepare, b = n.onLeavePrepare, x = n.onAppearStart, g = n.onEnterStart, h = n.onLeaveStart, E = n.onAppearActive, T = n.onEnterActive, S = n.onLeaveActive, w = n.onAppearEnd, v = n.onEnterEnd, _ = n.onLeaveEnd, y = n.onVisibleChanged, L = Ce(), F = W(L, 2), k = F[0], P = F[1], O = ai(ie), $ = W(O, 2), A = $[0], j = $[1], z = Ce(null), q = W(z, 2), fe = q[0], oe = q[1], V = A(), D = se(!1), G = se(null);
  function N() {
    return r();
  }
  var K = se(!1);
  function ae() {
    j(ie), oe(null, !0);
  }
  var re = ve(function(Z) {
    var U = A();
    if (U !== ie) {
      var ee = N();
      if (!(Z && !Z.deadline && Z.target !== ee)) {
        var Me = K.current, Ie;
        U === Oe && Me ? Ie = w == null ? void 0 : w(ee, Z) : U === $e && Me ? Ie = v == null ? void 0 : v(ee, Z) : U === Ae && Me && (Ie = _ == null ? void 0 : _(ee, Z)), Me && Ie !== !1 && ae();
      }
    }
  }), ot = fi(re), Re = W(ot, 1), Te = Re[0], Le = function(U) {
    switch (U) {
      case Oe:
        return R(R(R({}, J, d), me, x), ge, E);
      case $e:
        return R(R(R({}, J, m), me, g), ge, T);
      case Ae:
        return R(R(R({}, J, b), me, h), ge, S);
      default:
        return {};
    }
  }, le = M.useMemo(function() {
    return Le(V);
  }, [V]), Pe = hi(V, !e, function(Z) {
    if (Z === J) {
      var U = le[J];
      return U ? U(N()) : Zr;
    }
    if (ce in le) {
      var ee;
      oe(((ee = le[ce]) === null || ee === void 0 ? void 0 : ee.call(le, N(), null)) || null);
    }
    return ce === ge && V !== ie && (Te(N()), p > 0 && (clearTimeout(G.current), G.current = setTimeout(function() {
      re({
        deadline: !0
      });
    }, p))), ce === zr && ae(), gi;
  }), jt = W(Pe, 2), ln = jt[0], ce = jt[1], cn = Qr(ce);
  K.current = cn;
  var Dt = se(null);
  Wr(function() {
    if (!(D.current && Dt.current === t)) {
      P(t);
      var Z = D.current;
      D.current = !0;
      var U;
      !Z && t && a && (U = Oe), Z && t && i && (U = $e), (Z && !t && u || !Z && f && !t && u) && (U = Ae);
      var ee = Le(U);
      U && (e || ee[J]) ? (j(U), ln()) : j(ie), Dt.current = t;
    }
  }, [t]), xe(function() {
    // Cancel appear
    (V === Oe && !a || // Cancel enter
    V === $e && !i || // Cancel leave
    V === Ae && !u) && j(ie);
  }, [a, i, u]), xe(function() {
    return function() {
      D.current = !1, clearTimeout(G.current);
    };
  }, []);
  var it = M.useRef(!1);
  xe(function() {
    k && (it.current = !0), k !== void 0 && V === ie && ((it.current || k) && (y == null || y(k)), it.current = !0);
  }, [k, V]);
  var st = fe;
  return le[J] && ce === me && (st = C({
    transition: "none"
  }, st)), [V, ce, st, k ?? t];
}
function bi(e) {
  var t = e;
  B(e) === "object" && (t = e.transitionSupport);
  function r(o, i) {
    return !!(o.motionName && t && i !== !1);
  }
  var n = /* @__PURE__ */ M.forwardRef(function(o, i) {
    var s = o.visible, a = s === void 0 ? !0 : s, c = o.removeOnLeave, u = c === void 0 ? !0 : c, p = o.forceRender, f = o.children, d = o.motionName, m = o.leavedClassName, b = o.eventProps, x = M.useContext(oi), g = x.motion, h = r(o, g), E = se(), T = se();
    function S() {
      try {
        return E.current instanceof HTMLElement ? E.current : ri(T.current);
      } catch {
        return null;
      }
    }
    var w = vi(h, a, S, o), v = W(w, 4), _ = v[0], y = v[1], L = v[2], F = v[3], k = M.useRef(F);
    F && (k.current = !0);
    var P = M.useCallback(function(q) {
      E.current = q, Qo(i, q);
    }, [i]), O, $ = C(C({}, b), {}, {
      visible: a
    });
    if (!f)
      O = null;
    else if (_ === ie)
      F ? O = f(C({}, $), P) : !u && k.current && m ? O = f(C(C({}, $), {}, {
        className: m
      }), P) : p || !u && !m ? O = f(C(C({}, $), {}, {
        style: {
          display: "none"
        }
      }), P) : O = null;
    else {
      var A;
      y === J ? A = "prepare" : Qr(y) ? A = "active" : y === me && (A = "start");
      var j = hr(d, "".concat(_, "-").concat(A));
      O = f(C(C({}, $), {}, {
        className: Q(hr(d, _), R(R({}, j, j && A), d, typeof d == "string")),
        style: L
      }), P);
    }
    if (/* @__PURE__ */ M.isValidElement(O) && Yo(O)) {
      var z = Jo(O);
      z || (O = /* @__PURE__ */ M.cloneElement(O, {
        ref: P
      }));
    }
    return /* @__PURE__ */ M.createElement(si, {
      ref: T
    }, O);
  });
  return n.displayName = "CSSMotion", n;
}
const yi = bi(Xr);
var _t = "add", Rt = "keep", Tt = "remove", gt = "removed";
function Si(e) {
  var t;
  return e && B(e) === "object" && "key" in e ? t = e : t = {
    key: e
  }, C(C({}, t), {}, {
    key: String(t.key)
  });
}
function Lt() {
  var e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [];
  return e.map(Si);
}
function xi() {
  var e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [], t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : [], r = [], n = 0, o = t.length, i = Lt(e), s = Lt(t);
  i.forEach(function(u) {
    for (var p = !1, f = n; f < o; f += 1) {
      var d = s[f];
      if (d.key === u.key) {
        n < f && (r = r.concat(s.slice(n, f).map(function(m) {
          return C(C({}, m), {}, {
            status: _t
          });
        })), n = f), r.push(C(C({}, d), {}, {
          status: Rt
        })), n += 1, p = !0;
        break;
      }
    }
    p || r.push(C(C({}, u), {}, {
      status: Tt
    }));
  }), n < o && (r = r.concat(s.slice(n).map(function(u) {
    return C(C({}, u), {}, {
      status: _t
    });
  })));
  var a = {};
  r.forEach(function(u) {
    var p = u.key;
    a[p] = (a[p] || 0) + 1;
  });
  var c = Object.keys(a).filter(function(u) {
    return a[u] > 1;
  });
  return c.forEach(function(u) {
    r = r.filter(function(p) {
      var f = p.key, d = p.status;
      return f !== u || d !== Tt;
    }), r.forEach(function(p) {
      p.key === u && (p.status = Rt);
    });
  }), r;
}
var wi = ["component", "children", "onVisibleChanged", "onAllRemoved"], Ei = ["status"], Ci = ["eventProps", "visible", "children", "motionName", "motionAppear", "motionEnter", "motionLeave", "motionLeaveImmediately", "motionDeadline", "removeOnLeave", "leavedClassName", "onAppearPrepare", "onAppearStart", "onAppearActive", "onAppearEnd", "onEnterStart", "onEnterActive", "onEnterEnd", "onLeaveStart", "onLeaveActive", "onLeaveEnd"];
function _i(e) {
  var t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : yi, r = /* @__PURE__ */ function(n) {
    rt(i, n);
    var o = nt(i);
    function i() {
      var s;
      be(this, i);
      for (var a = arguments.length, c = new Array(a), u = 0; u < a; u++)
        c[u] = arguments[u];
      return s = o.call.apply(o, [this].concat(c)), R(ue(s), "state", {
        keyEntities: []
      }), R(ue(s), "removeKey", function(p) {
        s.setState(function(f) {
          var d = f.keyEntities.map(function(m) {
            return m.key !== p ? m : C(C({}, m), {}, {
              status: gt
            });
          });
          return {
            keyEntities: d
          };
        }, function() {
          var f = s.state.keyEntities, d = f.filter(function(m) {
            var b = m.status;
            return b !== gt;
          }).length;
          d === 0 && s.props.onAllRemoved && s.props.onAllRemoved();
        });
      }), s;
    }
    return ye(i, [{
      key: "render",
      value: function() {
        var a = this, c = this.state.keyEntities, u = this.props, p = u.component, f = u.children, d = u.onVisibleChanged;
        u.onAllRemoved;
        var m = ur(u, wi), b = p || M.Fragment, x = {};
        return Ci.forEach(function(g) {
          x[g] = m[g], delete m[g];
        }), delete m.keys, /* @__PURE__ */ M.createElement(b, m, c.map(function(g, h) {
          var E = g.status, T = ur(g, Ei), S = E === _t || E === Rt;
          return /* @__PURE__ */ M.createElement(t, he({}, x, {
            key: T.key,
            visible: S,
            eventProps: T,
            onVisibleChanged: function(v) {
              d == null || d(v, {
                key: T.key
              }), v || a.removeKey(T.key);
            }
          }), function(w, v) {
            return f(C(C({}, w), {}, {
              index: h
            }), v);
          });
        }));
      }
    }], [{
      key: "getDerivedStateFromProps",
      value: function(a, c) {
        var u = a.keys, p = c.keyEntities, f = Lt(u), d = xi(p, f);
        return {
          keyEntities: d.filter(function(m) {
            var b = p.find(function(x) {
              var g = x.key;
              return m.key === g;
            });
            return !(b && b.status === gt && m.status === Tt);
          })
        };
      }
    }]), i;
  }(M.Component);
  return R(r, "defaultProps", {
    component: "div"
  }), r;
}
const Ri = _i(Xr);
function Ti(e, t) {
  const {
    children: r,
    upload: n,
    rootClassName: o
  } = e, i = l.useRef(null);
  return l.useImperativeHandle(t, () => i.current), /* @__PURE__ */ l.createElement(Lr, he({}, n, {
    showUploadList: !1,
    rootClassName: o,
    ref: i
  }), r);
}
const Yr = /* @__PURE__ */ l.forwardRef(Ti);
var Jr = /* @__PURE__ */ ye(function e() {
  be(this, e);
}), en = "CALC_UNIT", Li = new RegExp(en, "g");
function ht(e) {
  return typeof e == "number" ? "".concat(e).concat(en) : e;
}
var Pi = /* @__PURE__ */ function(e) {
  rt(r, e);
  var t = nt(r);
  function r(n, o) {
    var i;
    be(this, r), i = t.call(this), R(ue(i), "result", ""), R(ue(i), "unitlessCssVar", void 0), R(ue(i), "lowPriority", void 0);
    var s = B(n);
    return i.unitlessCssVar = o, n instanceof r ? i.result = "(".concat(n.result, ")") : s === "number" ? i.result = ht(n) : s === "string" && (i.result = n), i;
  }
  return ye(r, [{
    key: "add",
    value: function(o) {
      return o instanceof r ? this.result = "".concat(this.result, " + ").concat(o.getResult()) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " + ").concat(ht(o))), this.lowPriority = !0, this;
    }
  }, {
    key: "sub",
    value: function(o) {
      return o instanceof r ? this.result = "".concat(this.result, " - ").concat(o.getResult()) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " - ").concat(ht(o))), this.lowPriority = !0, this;
    }
  }, {
    key: "mul",
    value: function(o) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), o instanceof r ? this.result = "".concat(this.result, " * ").concat(o.getResult(!0)) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " * ").concat(o)), this.lowPriority = !1, this;
    }
  }, {
    key: "div",
    value: function(o) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), o instanceof r ? this.result = "".concat(this.result, " / ").concat(o.getResult(!0)) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " / ").concat(o)), this.lowPriority = !1, this;
    }
  }, {
    key: "getResult",
    value: function(o) {
      return this.lowPriority || o ? "(".concat(this.result, ")") : this.result;
    }
  }, {
    key: "equal",
    value: function(o) {
      var i = this, s = o || {}, a = s.unit, c = !0;
      return typeof a == "boolean" ? c = a : Array.from(this.unitlessCssVar).some(function(u) {
        return i.result.includes(u);
      }) && (c = !1), this.result = this.result.replace(Li, c ? "px" : ""), typeof this.lowPriority < "u" ? "calc(".concat(this.result, ")") : this.result;
    }
  }]), r;
}(Jr), Mi = /* @__PURE__ */ function(e) {
  rt(r, e);
  var t = nt(r);
  function r(n) {
    var o;
    return be(this, r), o = t.call(this), R(ue(o), "result", 0), n instanceof r ? o.result = n.result : typeof n == "number" && (o.result = n), o;
  }
  return ye(r, [{
    key: "add",
    value: function(o) {
      return o instanceof r ? this.result += o.result : typeof o == "number" && (this.result += o), this;
    }
  }, {
    key: "sub",
    value: function(o) {
      return o instanceof r ? this.result -= o.result : typeof o == "number" && (this.result -= o), this;
    }
  }, {
    key: "mul",
    value: function(o) {
      return o instanceof r ? this.result *= o.result : typeof o == "number" && (this.result *= o), this;
    }
  }, {
    key: "div",
    value: function(o) {
      return o instanceof r ? this.result /= o.result : typeof o == "number" && (this.result /= o), this;
    }
  }, {
    key: "equal",
    value: function() {
      return this.result;
    }
  }]), r;
}(Jr), Ii = function(t, r) {
  var n = t === "css" ? Pi : Mi;
  return function(o) {
    return new n(o, r);
  };
}, br = function(t, r) {
  return "".concat([r, t.replace(/([A-Z]+)([A-Z][a-z]+)/g, "$1-$2").replace(/([a-z])([A-Z])/g, "$1-$2")].filter(Boolean).join("-"));
};
function yr(e, t, r, n) {
  var o = C({}, t[e]);
  if (n != null && n.deprecatedTokens) {
    var i = n.deprecatedTokens;
    i.forEach(function(a) {
      var c = W(a, 2), u = c[0], p = c[1];
      if (o != null && o[u] || o != null && o[p]) {
        var f;
        (f = o[p]) !== null && f !== void 0 || (o[p] = o == null ? void 0 : o[u]);
      }
    });
  }
  var s = C(C({}, r), o);
  return Object.keys(s).forEach(function(a) {
    s[a] === t[a] && delete s[a];
  }), s;
}
var tn = typeof CSSINJS_STATISTIC < "u", Pt = !0;
function kt() {
  for (var e = arguments.length, t = new Array(e), r = 0; r < e; r++)
    t[r] = arguments[r];
  if (!tn)
    return Object.assign.apply(Object, [{}].concat(t));
  Pt = !1;
  var n = {};
  return t.forEach(function(o) {
    if (B(o) === "object") {
      var i = Object.keys(o);
      i.forEach(function(s) {
        Object.defineProperty(n, s, {
          configurable: !0,
          enumerable: !0,
          get: function() {
            return o[s];
          }
        });
      });
    }
  }), Pt = !0, n;
}
var Sr = {};
function Oi() {
}
var $i = function(t) {
  var r, n = t, o = Oi;
  return tn && typeof Proxy < "u" && (r = /* @__PURE__ */ new Set(), n = new Proxy(t, {
    get: function(s, a) {
      if (Pt) {
        var c;
        (c = r) === null || c === void 0 || c.add(a);
      }
      return s[a];
    }
  }), o = function(s, a) {
    var c;
    Sr[s] = {
      global: Array.from(r),
      component: C(C({}, (c = Sr[s]) === null || c === void 0 ? void 0 : c.component), a)
    };
  }), {
    token: n,
    keys: r,
    flush: o
  };
};
function xr(e, t, r) {
  if (typeof r == "function") {
    var n;
    return r(kt(t, (n = t[e]) !== null && n !== void 0 ? n : {}));
  }
  return r ?? {};
}
function Ai(e) {
  return e === "js" ? {
    max: Math.max,
    min: Math.min
  } : {
    max: function() {
      for (var r = arguments.length, n = new Array(r), o = 0; o < r; o++)
        n[o] = arguments[o];
      return "max(".concat(n.map(function(i) {
        return Ut(i);
      }).join(","), ")");
    },
    min: function() {
      for (var r = arguments.length, n = new Array(r), o = 0; o < r; o++)
        n[o] = arguments[o];
      return "min(".concat(n.map(function(i) {
        return Ut(i);
      }).join(","), ")");
    }
  };
}
var Fi = 1e3 * 60 * 10, ki = /* @__PURE__ */ function() {
  function e() {
    be(this, e), R(this, "map", /* @__PURE__ */ new Map()), R(this, "objectIDMap", /* @__PURE__ */ new WeakMap()), R(this, "nextID", 0), R(this, "lastAccessBeat", /* @__PURE__ */ new Map()), R(this, "accessBeat", 0);
  }
  return ye(e, [{
    key: "set",
    value: function(r, n) {
      this.clear();
      var o = this.getCompositeKey(r);
      this.map.set(o, n), this.lastAccessBeat.set(o, Date.now());
    }
  }, {
    key: "get",
    value: function(r) {
      var n = this.getCompositeKey(r), o = this.map.get(n);
      return this.lastAccessBeat.set(n, Date.now()), this.accessBeat += 1, o;
    }
  }, {
    key: "getCompositeKey",
    value: function(r) {
      var n = this, o = r.map(function(i) {
        return i && B(i) === "object" ? "obj_".concat(n.getObjectID(i)) : "".concat(B(i), "_").concat(i);
      });
      return o.join("|");
    }
  }, {
    key: "getObjectID",
    value: function(r) {
      if (this.objectIDMap.has(r))
        return this.objectIDMap.get(r);
      var n = this.nextID;
      return this.objectIDMap.set(r, n), this.nextID += 1, n;
    }
  }, {
    key: "clear",
    value: function() {
      var r = this;
      if (this.accessBeat > 1e4) {
        var n = Date.now();
        this.lastAccessBeat.forEach(function(o, i) {
          n - o > Fi && (r.map.delete(i), r.lastAccessBeat.delete(i));
        }), this.accessBeat = 0;
      }
    }
  }]), e;
}(), wr = new ki();
function ji(e, t) {
  return l.useMemo(function() {
    var r = wr.get(t);
    if (r)
      return r;
    var n = e();
    return wr.set(t, n), n;
  }, t);
}
var Di = function() {
  return {};
};
function Ni(e) {
  var t = e.useCSP, r = t === void 0 ? Di : t, n = e.useToken, o = e.usePrefix, i = e.getResetStyles, s = e.getCommonStyle, a = e.getCompUnitless;
  function c(d, m, b, x) {
    var g = Array.isArray(d) ? d[0] : d;
    function h(y) {
      return "".concat(String(g)).concat(y.slice(0, 1).toUpperCase()).concat(y.slice(1));
    }
    var E = (x == null ? void 0 : x.unitless) || {}, T = typeof a == "function" ? a(d) : {}, S = C(C({}, T), {}, R({}, h("zIndexPopup"), !0));
    Object.keys(E).forEach(function(y) {
      S[h(y)] = E[y];
    });
    var w = C(C({}, x), {}, {
      unitless: S,
      prefixToken: h
    }), v = p(d, m, b, w), _ = u(g, b, w);
    return function(y) {
      var L = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : y, F = v(y, L), k = W(F, 2), P = k[1], O = _(L), $ = W(O, 2), A = $[0], j = $[1];
      return [A, P, j];
    };
  }
  function u(d, m, b) {
    var x = b.unitless, g = b.injectStyle, h = g === void 0 ? !0 : g, E = b.prefixToken, T = b.ignore, S = function(_) {
      var y = _.rootCls, L = _.cssVar, F = L === void 0 ? {} : L, k = n(), P = k.realToken;
      return jn({
        path: [d],
        prefix: F.prefix,
        key: F.key,
        unitless: x,
        ignore: T,
        token: P,
        scope: y
      }, function() {
        var O = xr(d, P, m), $ = yr(d, P, O, {
          deprecatedTokens: b == null ? void 0 : b.deprecatedTokens
        });
        return Object.keys(O).forEach(function(A) {
          $[E(A)] = $[A], delete $[A];
        }), $;
      }), null;
    }, w = function(_) {
      var y = n(), L = y.cssVar;
      return [function(F) {
        return h && L ? /* @__PURE__ */ l.createElement(l.Fragment, null, /* @__PURE__ */ l.createElement(S, {
          rootCls: _,
          cssVar: L,
          component: d
        }), F) : F;
      }, L == null ? void 0 : L.key];
    };
    return w;
  }
  function p(d, m, b) {
    var x = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, g = Array.isArray(d) ? d : [d, d], h = W(g, 1), E = h[0], T = g.join("-"), S = e.layer || {
      name: "antd"
    };
    return function(w) {
      var v = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : w, _ = n(), y = _.theme, L = _.realToken, F = _.hashId, k = _.token, P = _.cssVar, O = o(), $ = O.rootPrefixCls, A = O.iconPrefixCls, j = r(), z = P ? "css" : "js", q = ji(function() {
        var N = /* @__PURE__ */ new Set();
        return P && Object.keys(x.unitless || {}).forEach(function(K) {
          N.add(ct(K, P.prefix)), N.add(ct(K, br(E, P.prefix)));
        }), Ii(z, N);
      }, [z, E, P == null ? void 0 : P.prefix]), fe = Ai(z), oe = fe.max, V = fe.min, D = {
        theme: y,
        token: k,
        hashId: F,
        nonce: function() {
          return j.nonce;
        },
        clientOnly: x.clientOnly,
        layer: S,
        // antd is always at top of styles
        order: x.order || -999
      };
      typeof i == "function" && Xt(C(C({}, D), {}, {
        clientOnly: !1,
        path: ["Shared", $]
      }), function() {
        return i(k, {
          prefix: {
            rootPrefixCls: $,
            iconPrefixCls: A
          },
          csp: j
        });
      });
      var G = Xt(C(C({}, D), {}, {
        path: [T, w, A]
      }), function() {
        if (x.injectStyle === !1)
          return [];
        var N = $i(k), K = N.token, ae = N.flush, re = xr(E, L, b), ot = ".".concat(w), Re = yr(E, L, re, {
          deprecatedTokens: x.deprecatedTokens
        });
        P && re && B(re) === "object" && Object.keys(re).forEach(function(Pe) {
          re[Pe] = "var(".concat(ct(Pe, br(E, P.prefix)), ")");
        });
        var Te = kt(K, {
          componentCls: ot,
          prefixCls: w,
          iconCls: ".".concat(A),
          antCls: ".".concat($),
          calc: q,
          // @ts-ignore
          max: oe,
          // @ts-ignore
          min: V
        }, P ? re : Re), Le = m(Te, {
          hashId: F,
          prefixCls: w,
          rootPrefixCls: $,
          iconPrefixCls: A
        });
        ae(E, Re);
        var le = typeof s == "function" ? s(Te, w, v, x.resetFont) : null;
        return [x.resetStyle === !1 ? null : le, Le];
      });
      return [G, F];
    };
  }
  function f(d, m, b) {
    var x = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, g = p(d, m, b, C({
      resetStyle: !1,
      // Sub Style should default after root one
      order: -998
    }, x)), h = function(T) {
      var S = T.prefixCls, w = T.rootCls, v = w === void 0 ? S : w;
      return g(S, v), null;
    };
    return h;
  }
  return {
    genStyleHooks: c,
    genSubStyleComponent: f,
    genComponentStyleHook: p
  };
}
const H = Math.round;
function vt(e, t) {
  const r = e.replace(/^[^(]*\((.*)/, "$1").replace(/\).*/, "").match(/\d*\.?\d+%?/g) || [], n = r.map((o) => parseFloat(o));
  for (let o = 0; o < 3; o += 1)
    n[o] = t(n[o] || 0, r[o] || "", o);
  return r[3] ? n[3] = r[3].includes("%") ? n[3] / 100 : n[3] : n[3] = 1, n;
}
const Er = (e, t, r) => r === 0 ? e : e / 100;
function Se(e, t) {
  const r = t || 255;
  return e > r ? r : e < 0 ? 0 : e;
}
class te {
  constructor(t) {
    R(this, "isValid", !0), R(this, "r", 0), R(this, "g", 0), R(this, "b", 0), R(this, "a", 1), R(this, "_h", void 0), R(this, "_s", void 0), R(this, "_l", void 0), R(this, "_v", void 0), R(this, "_max", void 0), R(this, "_min", void 0), R(this, "_brightness", void 0);
    function r(n) {
      return n[0] in t && n[1] in t && n[2] in t;
    }
    if (t) if (typeof t == "string") {
      let o = function(i) {
        return n.startsWith(i);
      };
      const n = t.trim();
      /^#?[A-F\d]{3,8}$/i.test(n) ? this.fromHexString(n) : o("rgb") ? this.fromRgbString(n) : o("hsl") ? this.fromHslString(n) : (o("hsv") || o("hsb")) && this.fromHsvString(n);
    } else if (t instanceof te)
      this.r = t.r, this.g = t.g, this.b = t.b, this.a = t.a, this._h = t._h, this._s = t._s, this._l = t._l, this._v = t._v;
    else if (r("rgb"))
      this.r = Se(t.r), this.g = Se(t.g), this.b = Se(t.b), this.a = typeof t.a == "number" ? Se(t.a, 1) : 1;
    else if (r("hsl"))
      this.fromHsl(t);
    else if (r("hsv"))
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
    const r = this.toHsv();
    return r.h = t, this._c(r);
  }
  // ======================= Getter =======================
  /**
   * Returns the perceived luminance of a color, from 0-1.
   * @see http://www.w3.org/TR/2008/REC-WCAG20-20081211/#relativeluminancedef
   */
  getLuminance() {
    function t(i) {
      const s = i / 255;
      return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
    }
    const r = t(this.r), n = t(this.g), o = t(this.b);
    return 0.2126 * r + 0.7152 * n + 0.0722 * o;
  }
  getHue() {
    if (typeof this._h > "u") {
      const t = this.getMax() - this.getMin();
      t === 0 ? this._h = 0 : this._h = H(60 * (this.r === this.getMax() ? (this.g - this.b) / t + (this.g < this.b ? 6 : 0) : this.g === this.getMax() ? (this.b - this.r) / t + 2 : (this.r - this.g) / t + 4));
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
    const r = this.getHue(), n = this.getSaturation();
    let o = this.getLightness() - t / 100;
    return o < 0 && (o = 0), this._c({
      h: r,
      s: n,
      l: o,
      a: this.a
    });
  }
  lighten(t = 10) {
    const r = this.getHue(), n = this.getSaturation();
    let o = this.getLightness() + t / 100;
    return o > 1 && (o = 1), this._c({
      h: r,
      s: n,
      l: o,
      a: this.a
    });
  }
  /**
   * Mix the current color a given amount with another color, from 0 to 100.
   * 0 means no mixing (return current color).
   */
  mix(t, r = 50) {
    const n = this._c(t), o = r / 100, i = (a) => (n[a] - this[a]) * o + this[a], s = {
      r: H(i("r")),
      g: H(i("g")),
      b: H(i("b")),
      a: H(i("a") * 100) / 100
    };
    return this._c(s);
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
    const r = this._c(t), n = this.a + r.a * (1 - this.a), o = (i) => H((this[i] * this.a + r[i] * r.a * (1 - this.a)) / n);
    return this._c({
      r: o("r"),
      g: o("g"),
      b: o("b"),
      a: n
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
    const r = (this.r || 0).toString(16);
    t += r.length === 2 ? r : "0" + r;
    const n = (this.g || 0).toString(16);
    t += n.length === 2 ? n : "0" + n;
    const o = (this.b || 0).toString(16);
    if (t += o.length === 2 ? o : "0" + o, typeof this.a == "number" && this.a >= 0 && this.a < 1) {
      const i = H(this.a * 255).toString(16);
      t += i.length === 2 ? i : "0" + i;
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
    const t = this.getHue(), r = H(this.getSaturation() * 100), n = H(this.getLightness() * 100);
    return this.a !== 1 ? `hsla(${t},${r}%,${n}%,${this.a})` : `hsl(${t},${r}%,${n}%)`;
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
  _sc(t, r, n) {
    const o = this.clone();
    return o[t] = Se(r, n), o;
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
    const r = t.replace("#", "");
    function n(o, i) {
      return parseInt(r[o] + r[i || o], 16);
    }
    r.length < 6 ? (this.r = n(0), this.g = n(1), this.b = n(2), this.a = r[3] ? n(3) / 255 : 1) : (this.r = n(0, 1), this.g = n(2, 3), this.b = n(4, 5), this.a = r[6] ? n(6, 7) / 255 : 1);
  }
  fromHsl({
    h: t,
    s: r,
    l: n,
    a: o
  }) {
    if (this._h = t % 360, this._s = r, this._l = n, this.a = typeof o == "number" ? o : 1, r <= 0) {
      const d = H(n * 255);
      this.r = d, this.g = d, this.b = d;
    }
    let i = 0, s = 0, a = 0;
    const c = t / 60, u = (1 - Math.abs(2 * n - 1)) * r, p = u * (1 - Math.abs(c % 2 - 1));
    c >= 0 && c < 1 ? (i = u, s = p) : c >= 1 && c < 2 ? (i = p, s = u) : c >= 2 && c < 3 ? (s = u, a = p) : c >= 3 && c < 4 ? (s = p, a = u) : c >= 4 && c < 5 ? (i = p, a = u) : c >= 5 && c < 6 && (i = u, a = p);
    const f = n - u / 2;
    this.r = H((i + f) * 255), this.g = H((s + f) * 255), this.b = H((a + f) * 255);
  }
  fromHsv({
    h: t,
    s: r,
    v: n,
    a: o
  }) {
    this._h = t % 360, this._s = r, this._v = n, this.a = typeof o == "number" ? o : 1;
    const i = H(n * 255);
    if (this.r = i, this.g = i, this.b = i, r <= 0)
      return;
    const s = t / 60, a = Math.floor(s), c = s - a, u = H(n * (1 - r) * 255), p = H(n * (1 - r * c) * 255), f = H(n * (1 - r * (1 - c)) * 255);
    switch (a) {
      case 0:
        this.g = f, this.b = u;
        break;
      case 1:
        this.r = p, this.b = u;
        break;
      case 2:
        this.r = u, this.b = f;
        break;
      case 3:
        this.r = u, this.g = p;
        break;
      case 4:
        this.r = f, this.g = u;
        break;
      case 5:
      default:
        this.g = u, this.b = p;
        break;
    }
  }
  fromHsvString(t) {
    const r = vt(t, Er);
    this.fromHsv({
      h: r[0],
      s: r[1],
      v: r[2],
      a: r[3]
    });
  }
  fromHslString(t) {
    const r = vt(t, Er);
    this.fromHsl({
      h: r[0],
      s: r[1],
      l: r[2],
      a: r[3]
    });
  }
  fromRgbString(t) {
    const r = vt(t, (n, o) => (
      // Convert percentage to number. e.g. 50% -> 128
      o.includes("%") ? H(n / 100 * 255) : n
    ));
    this.r = r[0], this.g = r[1], this.b = r[2], this.a = r[3];
  }
}
const zi = {
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
}, Hi = Object.assign(Object.assign({}, zi), {
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
function bt(e) {
  return e >= 0 && e <= 255;
}
function ke(e, t) {
  const {
    r,
    g: n,
    b: o,
    a: i
  } = new te(e).toRgb();
  if (i < 1)
    return e;
  const {
    r: s,
    g: a,
    b: c
  } = new te(t).toRgb();
  for (let u = 0.01; u <= 1; u += 0.01) {
    const p = Math.round((r - s * (1 - u)) / u), f = Math.round((n - a * (1 - u)) / u), d = Math.round((o - c * (1 - u)) / u);
    if (bt(p) && bt(f) && bt(d))
      return new te({
        r: p,
        g: f,
        b: d,
        a: Math.round(u * 100) / 100
      }).toRgbString();
  }
  return new te({
    r,
    g: n,
    b: o,
    a: 1
  }).toRgbString();
}
var Bi = function(e, t) {
  var r = {};
  for (var n in e) Object.prototype.hasOwnProperty.call(e, n) && t.indexOf(n) < 0 && (r[n] = e[n]);
  if (e != null && typeof Object.getOwnPropertySymbols == "function") for (var o = 0, n = Object.getOwnPropertySymbols(e); o < n.length; o++)
    t.indexOf(n[o]) < 0 && Object.prototype.propertyIsEnumerable.call(e, n[o]) && (r[n[o]] = e[n[o]]);
  return r;
};
function Vi(e) {
  const {
    override: t
  } = e, r = Bi(e, ["override"]), n = Object.assign({}, t);
  Object.keys(Hi).forEach((d) => {
    delete n[d];
  });
  const o = Object.assign(Object.assign({}, r), n), i = 480, s = 576, a = 768, c = 992, u = 1200, p = 1600;
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
    colorSplit: ke(o.colorBorderSecondary, o.colorBgContainer),
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
    colorErrorOutline: ke(o.colorErrorBg, o.colorBgContainer),
    colorWarningOutline: ke(o.colorWarningBg, o.colorBgContainer),
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
    controlOutline: ke(o.colorPrimaryBg, o.colorBgContainer),
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
    screenXS: i,
    screenXSMin: i,
    screenXSMax: s - 1,
    screenSM: s,
    screenSMMin: s,
    screenSMMax: a - 1,
    screenMD: a,
    screenMDMin: a,
    screenMDMax: c - 1,
    screenLG: c,
    screenLGMin: c,
    screenLGMax: u - 1,
    screenXL: u,
    screenXLMin: u,
    screenXLMax: p - 1,
    screenXXL: p,
    screenXXLMin: p,
    boxShadowPopoverArrow: "2px 2px 5px rgba(0, 0, 0, 0.05)",
    boxShadowCard: `
      0 1px 2px -2px ${new te("rgba(0, 0, 0, 0.16)").toRgbString()},
      0 3px 6px 0 ${new te("rgba(0, 0, 0, 0.12)").toRgbString()},
      0 5px 12px 4px ${new te("rgba(0, 0, 0, 0.09)").toRgbString()}
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
  }), n);
}
const Ui = {
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
}, Xi = {
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
}, Wi = Dn(Ee.defaultAlgorithm), Gi = {
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
}, rn = (e, t, r) => {
  const n = r.getDerivativeToken(e), {
    override: o,
    ...i
  } = t;
  let s = {
    ...n,
    override: o
  };
  return s = Vi(s), i && Object.entries(i).forEach(([a, c]) => {
    const {
      theme: u,
      ...p
    } = c;
    let f = p;
    u && (f = rn({
      ...s,
      ...p
    }, {
      override: p
    }, u)), s[a] = f;
  }), s;
};
function qi() {
  const {
    token: e,
    hashed: t,
    theme: r = Wi,
    override: n,
    cssVar: o
  } = l.useContext(Ee._internalContext), [i, s, a] = Nn(r, [Ee.defaultSeed, e], {
    salt: `${Ao}-${t || ""}`,
    override: n,
    getComputedToken: rn,
    cssVar: o && {
      prefix: o.prefix,
      key: o.key,
      unitless: Ui,
      ignore: Xi,
      preserve: Gi
    }
  });
  return [r, a, t ? s : "", i, o];
}
const {
  genStyleHooks: Ki
} = Ni({
  usePrefix: () => {
    const {
      getPrefixCls: e,
      iconPrefixCls: t
    } = Be();
    return {
      iconPrefixCls: t,
      rootPrefixCls: e()
    };
  },
  useToken: () => {
    const [e, t, r, n, o] = qi();
    return {
      theme: e,
      realToken: t,
      hashId: r,
      token: n,
      cssVar: o
    };
  },
  useCSP: () => {
    const {
      csp: e
    } = Be();
    return e ?? {};
  },
  layer: {
    name: "antdx",
    dependencies: ["antd"]
  }
}), Zi = (e) => {
  const {
    componentCls: t,
    calc: r
  } = e, n = `${t}-list-card`, o = r(e.fontSize).mul(e.lineHeight).mul(2).add(e.paddingSM).add(e.paddingSM).equal();
  return {
    [n]: {
      borderRadius: e.borderRadius,
      position: "relative",
      background: e.colorFillContent,
      borderWidth: e.lineWidth,
      borderStyle: "solid",
      borderColor: "transparent",
      flex: "none",
      // =============================== Desc ================================
      [`${n}-name,${n}-desc`]: {
        display: "flex",
        flexWrap: "nowrap",
        maxWidth: "100%"
      },
      [`${n}-ellipsis-prefix`]: {
        flex: "0 1 auto",
        minWidth: 0,
        overflow: "hidden",
        textOverflow: "ellipsis",
        whiteSpace: "nowrap"
      },
      [`${n}-ellipsis-suffix`]: {
        flex: "none"
      },
      // ============================= Overview ==============================
      "&-type-overview": {
        padding: r(e.paddingSM).sub(e.lineWidth).equal(),
        paddingInlineStart: r(e.padding).add(e.lineWidth).equal(),
        display: "flex",
        flexWrap: "nowrap",
        gap: e.paddingXS,
        alignItems: "flex-start",
        width: 236,
        // Icon
        [`${n}-icon`]: {
          fontSize: r(e.fontSizeLG).mul(2).equal(),
          lineHeight: 1,
          paddingTop: r(e.paddingXXS).mul(1.5).equal(),
          flex: "none"
        },
        // Content
        [`${n}-content`]: {
          flex: "auto",
          minWidth: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "stretch"
        },
        [`${n}-desc`]: {
          color: e.colorTextTertiary
        }
      },
      // ============================== Preview ==============================
      "&-type-preview": {
        width: o,
        height: o,
        lineHeight: 1,
        [`&:not(${n}-status-error)`]: {
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
        [`${n}-img-mask`]: {
          position: "absolute",
          inset: 0,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          background: `rgba(0, 0, 0, ${e.opacityLoading})`,
          borderRadius: "inherit"
        },
        // Error
        [`&${n}-status-error`]: {
          [`img, ${n}-img-mask`]: {
            borderRadius: r(e.borderRadius).sub(e.lineWidth).equal()
          },
          [`${n}-desc`]: {
            paddingInline: e.paddingXXS
          }
        },
        // Progress
        [`${n}-progress`]: {}
      },
      // ============================ Remove Icon ============================
      [`${n}-remove`]: {
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
      [`&:hover ${n}-remove`]: {
        display: "block"
      },
      // ============================== Status ===============================
      "&-status-error": {
        borderColor: e.colorError,
        [`${n}-desc`]: {
          color: e.colorError
        }
      },
      // ============================== Motion ===============================
      "&-motion": {
        transition: ["opacity", "width", "margin", "padding"].map((i) => `${i} ${e.motionDurationSlow}`).join(","),
        "&-appear-start": {
          width: 0,
          transition: "none"
        },
        "&-leave-active": {
          opacity: 0,
          width: 0,
          paddingInline: 0,
          borderInlineWidth: 0,
          marginInlineEnd: r(e.paddingSM).mul(-1).equal()
        }
      }
    }
  };
}, Mt = {
  "&, *": {
    boxSizing: "border-box"
  }
}, Qi = (e) => {
  const {
    componentCls: t,
    calc: r,
    antCls: n
  } = e, o = `${t}-drop-area`, i = `${t}-placeholder`;
  return {
    // ============================== Full Screen ==============================
    [o]: {
      position: "absolute",
      inset: 0,
      zIndex: e.zIndexPopupBase,
      ...Mt,
      "&-on-body": {
        position: "fixed",
        inset: 0
      },
      "&-hide-placement": {
        [`${i}-inner`]: {
          display: "none"
        }
      },
      [i]: {
        padding: 0
      }
    },
    "&": {
      // ============================= Placeholder =============================
      [i]: {
        height: "100%",
        borderRadius: e.borderRadius,
        borderWidth: e.lineWidthBold,
        borderStyle: "dashed",
        borderColor: "transparent",
        padding: e.padding,
        position: "relative",
        backdropFilter: "blur(10px)",
        background: e.colorBgPlaceholderHover,
        ...Mt,
        [`${n}-upload-wrapper ${n}-upload${n}-upload-btn`]: {
          padding: 0
        },
        [`&${i}-drag-in`]: {
          borderColor: e.colorPrimaryHover
        },
        [`&${i}-disabled`]: {
          opacity: 0.25,
          pointerEvents: "none"
        },
        [`${i}-inner`]: {
          gap: r(e.paddingXXS).div(2).equal()
        },
        [`${i}-icon`]: {
          fontSize: e.fontSizeHeading2,
          lineHeight: 1
        },
        [`${i}-title${i}-title`]: {
          margin: 0,
          fontSize: e.fontSize,
          lineHeight: e.lineHeight
        },
        [`${i}-description`]: {}
      }
    }
  };
}, Yi = (e) => {
  const {
    componentCls: t,
    calc: r
  } = e, n = `${t}-list`, o = r(e.fontSize).mul(e.lineHeight).mul(2).add(e.paddingSM).add(e.paddingSM).equal();
  return {
    [t]: {
      position: "relative",
      width: "100%",
      ...Mt,
      // =============================== File List ===============================
      [n]: {
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
          maxHeight: r(o).mul(3).equal(),
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
          [`&${n}-overflow-ping-start ${n}-prev-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          },
          [`&${n}-overflow-ping-end ${n}-next-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          }
        },
        "&:dir(rtl)": {
          [`&${n}-overflow-ping-end ${n}-prev-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          },
          [`&${n}-overflow-ping-start ${n}-next-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          }
        }
      }
    }
  };
}, Ji = (e) => {
  const {
    colorBgContainer: t
  } = e;
  return {
    colorBgPlaceholderHover: new te(t).setA(0.85).toRgbString()
  };
}, nn = Ki("Attachments", (e) => {
  const t = kt(e, {});
  return [Qi(t), Yi(t), Zi(t)];
}, Ji), es = (e) => e.indexOf("image/") === 0, je = 200;
function ts(e) {
  return new Promise((t) => {
    if (!e || !e.type || !es(e.type)) {
      t("");
      return;
    }
    const r = new Image();
    if (r.onload = () => {
      const {
        width: n,
        height: o
      } = r, i = n / o, s = i > 1 ? je : je * i, a = i > 1 ? je / i : je, c = document.createElement("canvas");
      c.width = s, c.height = a, c.style.cssText = `position: fixed; left: 0; top: 0; width: ${s}px; height: ${a}px; z-index: 9999; display: none;`, document.body.appendChild(c), c.getContext("2d").drawImage(r, 0, 0, s, a);
      const p = c.toDataURL();
      document.body.removeChild(c), window.URL.revokeObjectURL(r.src), t(p);
    }, r.crossOrigin = "anonymous", e.type.startsWith("image/svg+xml")) {
      const n = new FileReader();
      n.onload = () => {
        n.result && typeof n.result == "string" && (r.src = n.result);
      }, n.readAsDataURL(e);
    } else if (e.type.startsWith("image/gif")) {
      const n = new FileReader();
      n.onload = () => {
        n.result && t(n.result);
      }, n.readAsDataURL(e);
    } else
      r.src = window.URL.createObjectURL(e);
  });
}
function rs() {
  return /* @__PURE__ */ l.createElement("svg", {
    width: "1em",
    height: "1em",
    viewBox: "0 0 16 16",
    version: "1.1",
    xmlns: "http://www.w3.org/2000/svg"
    //xmlnsXlink="http://www.w3.org/1999/xlink"
  }, /* @__PURE__ */ l.createElement("title", null, "audio"), /* @__PURE__ */ l.createElement("g", {
    stroke: "none",
    strokeWidth: "1",
    fill: "none",
    fillRule: "evenodd"
  }, /* @__PURE__ */ l.createElement("path", {
    d: "M14.1178571,4.0125 C14.225,4.11964286 14.2857143,4.26428571 14.2857143,4.41607143 L14.2857143,15.4285714 C14.2857143,15.7446429 14.0303571,16 13.7142857,16 L2.28571429,16 C1.96964286,16 1.71428571,15.7446429 1.71428571,15.4285714 L1.71428571,0.571428571 C1.71428571,0.255357143 1.96964286,0 2.28571429,0 L9.86964286,0 C10.0214286,0 10.1678571,0.0607142857 10.275,0.167857143 L14.1178571,4.0125 Z M10.7315824,7.11216117 C10.7428131,7.15148751 10.7485063,7.19218979 10.7485063,7.23309113 L10.7485063,8.07742614 C10.7484199,8.27364959 10.6183424,8.44607275 10.4296853,8.50003683 L8.32984514,9.09986306 L8.32984514,11.7071803 C8.32986605,12.5367078 7.67249692,13.217028 6.84345686,13.2454634 L6.79068592,13.2463395 C6.12766108,13.2463395 5.53916361,12.8217001 5.33010655,12.1924966 C5.1210495,11.563293 5.33842118,10.8709227 5.86959669,10.4741173 C6.40077221,10.0773119 7.12636292,10.0652587 7.67042486,10.4442027 L7.67020842,7.74937024 L7.68449368,7.74937024 C7.72405122,7.59919041 7.83988806,7.48101083 7.98924584,7.4384546 L10.1880418,6.81004755 C10.42156,6.74340323 10.6648954,6.87865515 10.7315824,7.11216117 Z M9.60714286,1.31785714 L12.9678571,4.67857143 L9.60714286,4.67857143 L9.60714286,1.31785714 Z",
    fill: "currentColor"
  })));
}
function ns(e) {
  const {
    percent: t
  } = e, {
    token: r
  } = Ee.useToken();
  return /* @__PURE__ */ l.createElement(wn, {
    type: "circle",
    percent: t,
    size: r.fontSizeHeading2 * 2,
    strokeColor: "#FFF",
    trailColor: "rgba(255, 255, 255, 0.3)",
    format: (n) => /* @__PURE__ */ l.createElement("span", {
      style: {
        color: "#FFF"
      }
    }, (n || 0).toFixed(0), "%")
  });
}
function os() {
  return /* @__PURE__ */ l.createElement("svg", {
    width: "1em",
    height: "1em",
    viewBox: "0 0 16 16",
    version: "1.1",
    xmlns: "http://www.w3.org/2000/svg"
    // xmlnsXlink="http://www.w3.org/1999/xlink"
  }, /* @__PURE__ */ l.createElement("title", null, "video"), /* @__PURE__ */ l.createElement("g", {
    stroke: "none",
    strokeWidth: "1",
    fill: "none",
    fillRule: "evenodd"
  }, /* @__PURE__ */ l.createElement("path", {
    d: "M14.1178571,4.0125 C14.225,4.11964286 14.2857143,4.26428571 14.2857143,4.41607143 L14.2857143,15.4285714 C14.2857143,15.7446429 14.0303571,16 13.7142857,16 L2.28571429,16 C1.96964286,16 1.71428571,15.7446429 1.71428571,15.4285714 L1.71428571,0.571428571 C1.71428571,0.255357143 1.96964286,0 2.28571429,0 L9.86964286,0 C10.0214286,0 10.1678571,0.0607142857 10.275,0.167857143 L14.1178571,4.0125 Z M12.9678571,4.67857143 L9.60714286,1.31785714 L9.60714286,4.67857143 L12.9678571,4.67857143 Z M10.5379461,10.3101106 L6.68957555,13.0059749 C6.59910784,13.0693494 6.47439406,13.0473861 6.41101953,12.9569184 C6.3874624,12.9232903 6.37482581,12.8832269 6.37482581,12.8421686 L6.37482581,7.45043999 C6.37482581,7.33998304 6.46436886,7.25043999 6.57482581,7.25043999 C6.61588409,7.25043999 6.65594753,7.26307658 6.68957555,7.28663371 L10.5379461,9.98249803 C10.6284138,10.0458726 10.6503772,10.1705863 10.5870027,10.2610541 C10.5736331,10.2801392 10.5570312,10.2967411 10.5379461,10.3101106 Z",
    fill: "currentColor"
  })));
}
const yt = " ", It = "#8c8c8c", on = ["png", "jpg", "jpeg", "gif", "bmp", "webp", "svg"], is = [{
  icon: /* @__PURE__ */ l.createElement(Tn, null),
  color: "#22b35e",
  ext: ["xlsx", "xls"]
}, {
  icon: /* @__PURE__ */ l.createElement(Ln, null),
  color: It,
  ext: on
}, {
  icon: /* @__PURE__ */ l.createElement(Pn, null),
  color: It,
  ext: ["md", "mdx"]
}, {
  icon: /* @__PURE__ */ l.createElement(Mn, null),
  color: "#ff4d4f",
  ext: ["pdf"]
}, {
  icon: /* @__PURE__ */ l.createElement(In, null),
  color: "#ff6e31",
  ext: ["ppt", "pptx"]
}, {
  icon: /* @__PURE__ */ l.createElement(On, null),
  color: "#1677ff",
  ext: ["doc", "docx"]
}, {
  icon: /* @__PURE__ */ l.createElement($n, null),
  color: "#fab714",
  ext: ["zip", "rar", "7z", "tar", "gz"]
}, {
  icon: /* @__PURE__ */ l.createElement(os, null),
  color: "#ff4d4f",
  ext: ["mp4", "avi", "mov", "wmv", "flv", "mkv"]
}, {
  icon: /* @__PURE__ */ l.createElement(rs, null),
  color: "#8c8c8c",
  ext: ["mp3", "wav", "flac", "ape", "aac", "ogg"]
}];
function Cr(e, t) {
  return t.some((r) => e.toLowerCase() === `.${r}`);
}
function ss(e) {
  let t = e;
  const r = ["B", "KB", "MB", "GB", "TB", "PB", "EB"];
  let n = 0;
  for (; t >= 1024 && n < r.length - 1; )
    t /= 1024, n++;
  return `${t.toFixed(0)} ${r[n]}`;
}
function as(e, t) {
  const {
    prefixCls: r,
    item: n,
    onRemove: o,
    className: i,
    style: s,
    imageProps: a
  } = e, c = l.useContext(_e), {
    disabled: u
  } = c || {}, {
    name: p,
    size: f,
    percent: d,
    status: m = "done",
    description: b
  } = n, {
    getPrefixCls: x
  } = Be(), g = x("attachment", r), h = `${g}-list-card`, [E, T, S] = nn(g), [w, v] = l.useMemo(() => {
    const j = p || "", z = j.match(/^(.*)\.[^.]+$/);
    return z ? [z[1], j.slice(z[1].length)] : [j, ""];
  }, [p]), _ = l.useMemo(() => Cr(v, on), [v]), y = l.useMemo(() => b || (m === "uploading" ? `${d || 0}%` : m === "error" ? n.response || yt : f ? ss(f) : yt), [m, d]), [L, F] = l.useMemo(() => {
    for (const {
      ext: j,
      icon: z,
      color: q
    } of is)
      if (Cr(v, j))
        return [z, q];
    return [/* @__PURE__ */ l.createElement(_n, {
      key: "defaultIcon"
    }), It];
  }, [v]), [k, P] = l.useState();
  l.useEffect(() => {
    if (n.originFileObj) {
      let j = !0;
      return ts(n.originFileObj).then((z) => {
        j && P(z);
      }), () => {
        j = !1;
      };
    }
    P(void 0);
  }, [n.originFileObj]);
  let O = null;
  const $ = n.thumbUrl || n.url || k, A = _ && (n.originFileObj || $);
  return A ? O = /* @__PURE__ */ l.createElement(l.Fragment, null, $ && /* @__PURE__ */ l.createElement(En, he({}, a, {
    alt: "preview",
    src: $
  })), m !== "done" && /* @__PURE__ */ l.createElement("div", {
    className: `${h}-img-mask`
  }, m === "uploading" && d !== void 0 && /* @__PURE__ */ l.createElement(ns, {
    percent: d,
    prefixCls: h
  }), m === "error" && /* @__PURE__ */ l.createElement("div", {
    className: `${h}-desc`
  }, /* @__PURE__ */ l.createElement("div", {
    className: `${h}-ellipsis-prefix`
  }, y)))) : O = /* @__PURE__ */ l.createElement(l.Fragment, null, /* @__PURE__ */ l.createElement("div", {
    className: `${h}-icon`,
    style: {
      color: F
    }
  }, L), /* @__PURE__ */ l.createElement("div", {
    className: `${h}-content`
  }, /* @__PURE__ */ l.createElement("div", {
    className: `${h}-name`
  }, /* @__PURE__ */ l.createElement("div", {
    className: `${h}-ellipsis-prefix`
  }, w ?? yt), /* @__PURE__ */ l.createElement("div", {
    className: `${h}-ellipsis-suffix`
  }, v)), /* @__PURE__ */ l.createElement("div", {
    className: `${h}-desc`
  }, /* @__PURE__ */ l.createElement("div", {
    className: `${h}-ellipsis-prefix`
  }, y)))), E(/* @__PURE__ */ l.createElement("div", {
    className: Q(h, {
      [`${h}-status-${m}`]: m,
      [`${h}-type-preview`]: A,
      [`${h}-type-overview`]: !A
    }, i, T, S),
    style: s,
    ref: t
  }, O, !u && o && /* @__PURE__ */ l.createElement("button", {
    type: "button",
    className: `${h}-remove`,
    onClick: () => {
      o(n);
    }
  }, /* @__PURE__ */ l.createElement(Rn, null))));
}
const sn = /* @__PURE__ */ l.forwardRef(as), _r = 1;
function ls(e) {
  const {
    prefixCls: t,
    items: r,
    onRemove: n,
    overflow: o,
    upload: i,
    listClassName: s,
    listStyle: a,
    itemClassName: c,
    itemStyle: u,
    imageProps: p
  } = e, f = `${t}-list`, d = l.useRef(null), [m, b] = l.useState(!1), {
    disabled: x
  } = l.useContext(_e);
  l.useEffect(() => (b(!0), () => {
    b(!1);
  }), []);
  const [g, h] = l.useState(!1), [E, T] = l.useState(!1), S = () => {
    const y = d.current;
    y && (o === "scrollX" ? (h(Math.abs(y.scrollLeft) >= _r), T(y.scrollWidth - y.clientWidth - Math.abs(y.scrollLeft) >= _r)) : o === "scrollY" && (h(y.scrollTop !== 0), T(y.scrollHeight - y.clientHeight !== y.scrollTop)));
  };
  l.useEffect(() => {
    S();
  }, [o, r.length]);
  const w = (y) => {
    const L = d.current;
    L && L.scrollTo({
      left: L.scrollLeft + y * L.clientWidth,
      behavior: "smooth"
    });
  }, v = () => {
    w(-1);
  }, _ = () => {
    w(1);
  };
  return /* @__PURE__ */ l.createElement("div", {
    className: Q(f, {
      [`${f}-overflow-${e.overflow}`]: o,
      [`${f}-overflow-ping-start`]: g,
      [`${f}-overflow-ping-end`]: E
    }, s),
    ref: d,
    onScroll: S,
    style: a
  }, /* @__PURE__ */ l.createElement(Ri, {
    keys: r.map((y) => ({
      key: y.uid,
      item: y
    })),
    motionName: `${f}-card-motion`,
    component: !1,
    motionAppear: m,
    motionLeave: !0,
    motionEnter: !0
  }, ({
    key: y,
    item: L,
    className: F,
    style: k
  }) => /* @__PURE__ */ l.createElement(sn, {
    key: y,
    prefixCls: t,
    item: L,
    onRemove: n,
    className: Q(F, c),
    imageProps: p,
    style: {
      ...k,
      ...u
    }
  })), !x && /* @__PURE__ */ l.createElement(Yr, {
    upload: i
  }, /* @__PURE__ */ l.createElement(at, {
    className: `${f}-upload-btn`,
    type: "dashed"
  }, /* @__PURE__ */ l.createElement(An, {
    className: `${f}-upload-btn-icon`
  }))), o === "scrollX" && /* @__PURE__ */ l.createElement(l.Fragment, null, /* @__PURE__ */ l.createElement(at, {
    size: "small",
    shape: "circle",
    className: `${f}-prev-btn`,
    icon: /* @__PURE__ */ l.createElement(Fn, null),
    onClick: v
  }), /* @__PURE__ */ l.createElement(at, {
    size: "small",
    shape: "circle",
    className: `${f}-next-btn`,
    icon: /* @__PURE__ */ l.createElement(kn, null),
    onClick: _
  })));
}
function cs(e, t) {
  const {
    prefixCls: r,
    placeholder: n = {},
    upload: o,
    className: i,
    style: s
  } = e, a = `${r}-placeholder`, c = n || {}, {
    disabled: u
  } = l.useContext(_e), [p, f] = l.useState(!1), d = () => {
    f(!0);
  }, m = (g) => {
    g.currentTarget.contains(g.relatedTarget) || f(!1);
  }, b = () => {
    f(!1);
  }, x = /* @__PURE__ */ l.isValidElement(n) ? n : /* @__PURE__ */ l.createElement(Cn, {
    align: "center",
    justify: "center",
    vertical: !0,
    className: `${a}-inner`
  }, /* @__PURE__ */ l.createElement(lt.Text, {
    className: `${a}-icon`
  }, c.icon), /* @__PURE__ */ l.createElement(lt.Title, {
    className: `${a}-title`,
    level: 5
  }, c.title), /* @__PURE__ */ l.createElement(lt.Text, {
    className: `${a}-description`,
    type: "secondary"
  }, c.description));
  return /* @__PURE__ */ l.createElement("div", {
    className: Q(a, {
      [`${a}-drag-in`]: p,
      [`${a}-disabled`]: u
    }, i),
    onDragEnter: d,
    onDragLeave: m,
    onDrop: b,
    "aria-hidden": u,
    style: s
  }, /* @__PURE__ */ l.createElement(Lr.Dragger, he({
    showUploadList: !1
  }, o, {
    ref: t,
    style: {
      padding: 0,
      border: 0,
      background: "transparent"
    }
  }), x));
}
const us = /* @__PURE__ */ l.forwardRef(cs);
function fs(e, t) {
  const {
    prefixCls: r,
    rootClassName: n,
    rootStyle: o,
    className: i,
    style: s,
    items: a,
    children: c,
    getDropContainer: u,
    placeholder: p,
    onChange: f,
    onRemove: d,
    overflow: m,
    imageProps: b,
    disabled: x,
    classNames: g = {},
    styles: h = {},
    ...E
  } = e, {
    getPrefixCls: T,
    direction: S
  } = Be(), w = T("attachment", r), v = jo("attachments"), {
    classNames: _,
    styles: y
  } = v, L = l.useRef(null), F = l.useRef(null);
  l.useImperativeHandle(t, () => ({
    nativeElement: L.current,
    upload: (D) => {
      var N, K;
      const G = (K = (N = F.current) == null ? void 0 : N.nativeElement) == null ? void 0 : K.querySelector('input[type="file"]');
      if (G) {
        const ae = new DataTransfer();
        ae.items.add(D), G.files = ae.files, G.dispatchEvent(new Event("change", {
          bubbles: !0
        }));
      }
    }
  }));
  const [k, P, O] = nn(w), $ = Q(P, O), [A, j] = Vo([], {
    value: a
  }), z = ve((D) => {
    j(D.fileList), f == null || f(D);
  }), q = {
    ...E,
    fileList: A,
    onChange: z
  }, fe = (D) => Promise.resolve(typeof d == "function" ? d(D) : d).then((G) => {
    if (G === !1)
      return;
    const N = A.filter((K) => K.uid !== D.uid);
    z({
      file: {
        ...D,
        status: "removed"
      },
      fileList: N
    });
  });
  let oe;
  const V = (D, G, N) => {
    const K = typeof p == "function" ? p(D) : p;
    return /* @__PURE__ */ l.createElement(us, {
      placeholder: K,
      upload: q,
      prefixCls: w,
      className: Q(_.placeholder, g.placeholder),
      style: {
        ...y.placeholder,
        ...h.placeholder,
        ...G == null ? void 0 : G.style
      },
      ref: N
    });
  };
  if (c)
    oe = /* @__PURE__ */ l.createElement(l.Fragment, null, /* @__PURE__ */ l.createElement(Yr, {
      upload: q,
      rootClassName: n,
      ref: F
    }, c), /* @__PURE__ */ l.createElement(lr, {
      getDropContainer: u,
      prefixCls: w,
      className: Q($, n)
    }, V("drop")));
  else {
    const D = A.length > 0;
    oe = /* @__PURE__ */ l.createElement("div", {
      className: Q(w, $, {
        [`${w}-rtl`]: S === "rtl"
      }, i, n),
      style: {
        ...o,
        ...s
      },
      dir: S || "ltr",
      ref: L
    }, /* @__PURE__ */ l.createElement(ls, {
      prefixCls: w,
      items: A,
      onRemove: fe,
      overflow: m,
      upload: q,
      listClassName: Q(_.list, g.list),
      listStyle: {
        ...y.list,
        ...h.list,
        ...!D && {
          display: "none"
        }
      },
      itemClassName: Q(_.item, g.item),
      itemStyle: {
        ...y.item,
        ...h.item
      },
      imageProps: b
    }), V("inline", D ? {
      style: {
        display: "none"
      }
    } : {}, F), /* @__PURE__ */ l.createElement(lr, {
      getDropContainer: u || (() => L.current),
      prefixCls: w,
      className: $
    }, V("drop")));
  }
  return k(/* @__PURE__ */ l.createElement(_e.Provider, {
    value: {
      disabled: x
    }
  }, oe));
}
const an = /* @__PURE__ */ l.forwardRef(fs);
an.FileCard = sn;
new Intl.Collator(0, {
  numeric: 1
}).compare;
typeof process < "u" && process.versions && process.versions.node;
var ne;
class Ss extends TransformStream {
  /** Constructs a new instance. */
  constructor(r = {
    allowCR: !1
  }) {
    super({
      transform: (n, o) => {
        for (n = de(this, ne) + n; ; ) {
          const i = n.indexOf(`
`), s = r.allowCR ? n.indexOf("\r") : -1;
          if (s !== -1 && s !== n.length - 1 && (i === -1 || i - 1 > s)) {
            o.enqueue(n.slice(0, s)), n = n.slice(s + 1);
            continue;
          }
          if (i === -1) break;
          const a = n[i - 1] === "\r" ? i - 1 : i;
          o.enqueue(n.slice(0, a)), n = n.slice(i + 1);
        }
        Bt(this, ne, n);
      },
      flush: (n) => {
        if (de(this, ne) === "") return;
        const o = r.allowCR && de(this, ne).endsWith("\r") ? de(this, ne).slice(0, -1) : de(this, ne);
        n.enqueue(o);
      }
    });
    Ht(this, ne, "");
  }
}
ne = new WeakMap();
function ds(e) {
  try {
    const t = new URL(e);
    return t.protocol === "http:" || t.protocol === "https:";
  } catch {
    return !1;
  }
}
function ps() {
  const e = document.querySelector(".gradio-container");
  if (!e)
    return "";
  const t = e.className.match(/gradio-container-(.+)/);
  return t ? t[1] : "";
}
const ms = +ps()[0];
function Rr(e, t, r) {
  const n = ms >= 5 ? "gradio_api/" : "";
  return e == null ? r ? `/proxy=${r}${n}file=` : `${t}${n}file=` : ds(e) ? e : r ? `/proxy=${r}${n}file=${e}` : `${t}/${n}file=${e}`;
}
const gs = ({
  item: e,
  urlRoot: t,
  urlProxyUrl: r,
  ...n
}) => {
  var s, a;
  const {
    token: o
  } = Ee.useToken(), i = Tr(() => e ? typeof e == "string" ? {
    url: e.startsWith("http") ? e : Rr(e, t, r),
    uid: e,
    name: e.split("/").pop()
  } : {
    ...e,
    uid: e.uid || e.path || e.url,
    name: e.name || e.orig_name || (e.url || e.path).split("/").pop(),
    url: e.url || Rr(e.path, t, r)
  } : {}, [e, r, t]);
  return /* @__PURE__ */ X.jsx(an.FileCard, {
    ...n,
    imageProps: {
      ...n.imageProps,
      wrapperStyle: {
        width: "100%",
        height: "100%",
        ...(s = n.imageProps) == null ? void 0 : s.wrapperStyle
      },
      style: {
        width: "100%",
        height: "100%",
        objectFit: "contain",
        borderRadius: o.borderRadius,
        ...(a = n.imageProps) == null ? void 0 : a.style
      }
    },
    item: i
  });
};
function hs(e) {
  return typeof e == "object" && e !== null ? e : {};
}
const xs = Co(({
  setSlotParams: e,
  imageProps: t,
  slots: r,
  children: n,
  ...o
}) => {
  const i = hs(t == null ? void 0 : t.preview), s = r["imageProps.preview.mask"] || r["imageProps.preview.closeIcon"] || r["imageProps.preview.toolbarRender"] || r["imageProps.preview.imageRender"] || (t == null ? void 0 : t.preview) !== !1, a = dt(i.getContainer), c = dt(i.toolbarRender), u = dt(i.imageRender);
  return /* @__PURE__ */ X.jsxs(X.Fragment, {
    children: [/* @__PURE__ */ X.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ X.jsx(gs, {
      ...o,
      imageProps: {
        ...t,
        preview: s ? Io({
          ...i,
          getContainer: a,
          toolbarRender: r["imageProps.preview.toolbarRender"] ? nr({
            slots: r,
            key: "imageProps.preview.toolbarRender"
          }) : c,
          imageRender: r["imageProps.preview.imageRender"] ? nr({
            slots: r,
            key: "imageProps.preview.imageRender"
          }) : u,
          ...r["imageProps.preview.mask"] || Reflect.has(i, "mask") ? {
            mask: r["imageProps.preview.mask"] ? /* @__PURE__ */ X.jsx(we, {
              slot: r["imageProps.preview.mask"]
            }) : i.mask
          } : {},
          closeIcon: r["imageProps.preview.closeIcon"] ? /* @__PURE__ */ X.jsx(we, {
            slot: r["imageProps.preview.closeIcon"]
          }) : i.closeIcon
        }) : !1,
        placeholder: r["imageProps.placeholder"] ? /* @__PURE__ */ X.jsx(we, {
          slot: r["imageProps.placeholder"]
        }) : t == null ? void 0 : t.placeholder
      }
    })]
  });
});
export {
  xs as AttachmentsFileCard,
  xs as default
};
