// Club edit page: tag chips, person-chip initials, and the WYSIWYG editor for extra content.
window.addEventListener("load", async () => {
  // tags <select multiple> -> toggle chips; the hidden select still holds the value that gets submitted
  const tags = document.getElementById("id_tags");
  if (tags) {
    const box = document.createElement("div");
    box.className = "tag-chips";
    for (const opt of tags.options) {
      const chip = document.createElement("button");
      chip.type = "button";
      chip.className = "tag-chip";
      chip.textContent = opt.text;
      chip.setAttribute("aria-pressed", opt.selected);
      chip.onclick = () => chip.setAttribute("aria-pressed", (opt.selected = !opt.selected));
      box.append(chip);
    }
    tags.classList.add("chipified");
    tags.after(box);
    const add = document.getElementById("add_id_tags");
    if (add) box.append(add); // "+" right after the last chip
  }

  // initials on owner/supervisor/exec chips, including ones added later
  const addInitials = () => {
    for (const c of document.querySelectorAll(".select2-selection__choice:not(:has(.avatar))")) {
      const a = document.createElement("span");
      a.className = "avatar";
      a.textContent = (c.title || c.textContent.replace("×", "")).trim().charAt(0).toUpperCase();
      c.prepend(a);
    }
  };
  addInitials();
  new MutationObserver(addInitials).observe(document.getElementById("content-main"), { childList: true, subtree: true });

  // extra content: Toast UI WYSIWYG editor; the textarea keeps the Markdown that gets submitted
  const ta = document.querySelector("textarea.wysiwyg-md");
  if (ta) {
    // if the CDN is unreachable, the plain Markdown textarea stays visible so the field still works
    // the self-contained "all" build: jsdelivr's +esm pulls in a second prosemirror-model, which breaks Enter and tables
    const Editor = await new Promise((resolve, reject) => {
      const s = document.createElement("script");
      s.src = "https://uicdn.toast.com/editor/3.2.2/toastui-editor-all.min.js";
      s.onload = () => resolve(window.toastui.Editor);
      s.onerror = reject;
      document.head.append(s);
    });
    ta.style.display = "none";
    // tooltips in everyday words (Docs' names) instead of Markdown jargon
    Editor.setLanguage(["en", "en-US"], {
      Headings: "Text style",
      "Unordered list": "Bulleted list",
      "Ordered list": "Numbered list",
      Blockquote: "Quote",
      Line: "Divider line",
    });
    const host = document.createElement("div");
    ta.after(host);
    const field = ta.closest("form");
    const csrf = field.querySelector("[name=csrfmiddlewaretoken]").value;
    const editor = new Editor({
      el: host,
      ...(ta.value && { initialValue: ta.value }),
      initialEditType: "wysiwyg",
      hideModeSwitch: true,
      usageStatistics: false,
      height: "auto",
      minHeight: "320px",
      placeholder: "Tell students about your club: how to join, what you do, photos\u2026",
      theme: "light", // the admin stays light in dark mode
      toolbarItems: [["heading", "bold", "italic"], ["ul", "ol", "quote"], ["link", "image", "table", "hr"]],
      hooks: {
        async addImageBlobHook(blob, done) {
          const body = new FormData();
          body.append("markdown-image-upload", blob, blob.name || "image.png");
          try {
            const r = await fetch("/api/upload-image/", { method: "POST", body, headers: { "X-CSRFToken": csrf } });
            const j = await r.json().catch(() => ({}));
            if (j.link) return done(j.link, "");
            alert(j.error || j.detail || "Image upload failed.");
          } catch {
            alert("Image upload failed.");
          }
        },
      },
    });
    // write back on edits only, so opening and saving leaves existing content byte-for-byte
    editor.on("change", () => (ta.value = editor.getMarkdown()));

    // Docs-style toolbar state: Bold/Italic light up when on (including just toggled, before typing),
    // and the heading button names the current style. Data attributes, because Toast re-renders className.
    const view = editor.wwEditor.view;
    const bar = host.querySelector(".toastui-editor-defaultUI-toolbar");
    const LABELS = { 1: "Heading 1", 2: "Heading 2", 3: "Heading 3" };
    const sync = () => {
      const { storedMarks, selection } = view.state;
      const marks = storedMarks || selection.$from.marks();
      for (const [cls, mark] of [["bold", "strong"], ["italic", "emph"]]) {
        bar.querySelector(".toastui-editor-toolbar-icons." + cls)?.toggleAttribute("data-on", marks.some((m) => m.type.name === mark));
      }
      const block = selection.$from.parent;
      bar.querySelector(".toastui-editor-toolbar-icons.heading")?.setAttribute(
        "data-label",
        block.type.name === "heading" ? LABELS[block.attrs.level] || "Heading" : "Normal text",
      );
    };
    sync();
    editor.on("caretChange", sync);
    editor.on("change", sync);
    // toggling Bold with nothing selected only changes stored marks, which fires no caret event
    bar.addEventListener("click", () => setTimeout(sync));
    host.addEventListener("keyup", sync);

    // Docs-style link card on hover or when the caret is in a link: open, copy, edit, remove.
    // shortcut: shows the URL, not the page title/preview (that needs a server-side fetch of arbitrary URLs).
    const card = document.createElement("div");
    card.className = "link-card";
    card.hidden = true;
    card.innerHTML = `<div class="link-card-row">
        <span class="ms">link</span><a class="link-card-url" target="_blank" rel="noopener noreferrer"></a>
        <button type="button" data-act="copy" data-tip="Copy link"><span class="ms">content_copy</span></button>
        <button type="button" data-act="edit" data-tip="Edit link"><span class="ms">edit</span></button>
        <button type="button" data-act="remove" data-tip="Remove link"><span class="ms">link_off</span></button>
      </div>
      <div class="link-card-edit" hidden><input type="url" aria-label="Link address"><button type="button" data-act="apply">Apply</button></div>`;
    host.style.position = "relative";
    host.append(card);
    const urlEl = card.querySelector(".link-card-url");
    const editForm = card.querySelector(".link-card-edit");
    const editInput = editForm.querySelector("input");
    const linkType = view.state.schema.marks.link;
    let current = null; // the <a> the card is for
    let hideTimer;

    const range = (a) => {
      const from = view.posAtDOM(a, 0);
      return { from, to: from + a.textContent.length, mark: view.state.doc.resolve(from + 1).marks().find((m) => m.type === linkType) };
    };
    const show = (a) => {
      clearTimeout(hideTimer);
      if (current === a && !card.hidden) return;
      current = a;
      const href = a.getAttribute("href") || "";
      urlEl.textContent = href;
      urlEl.href = /^(https?:|mailto:)/i.test(href) ? href : "#";
      editForm.hidden = true;
      card.querySelector("[data-act=copy]").dataset.tip = "Copy link";
      const h = host.getBoundingClientRect();
      const r = a.getBoundingClientRect();
      card.style.top = r.bottom - h.top + 6 + "px";
      card.style.left = Math.max(0, Math.min(r.left - h.left, h.width - 380)) + "px";
      card.hidden = false;
    };
    const hide = () => {
      card.hidden = true;
      current = null;
    };
    const hideSoon = () => {
      clearTimeout(hideTimer);
      hideTimer = setTimeout(hide, 300);
    };

    const pm = host.querySelector(".toastui-editor-ww-container .ProseMirror");
    pm.addEventListener("mouseover", (e) => {
      const a = e.target.closest("a");
      if (a) show(a);
    });
    pm.addEventListener("mouseout", (e) => {
      if (e.target.closest("a") && editForm.hidden) hideSoon();
    });
    card.addEventListener("mouseenter", () => clearTimeout(hideTimer));
    card.addEventListener("mouseleave", () => editForm.hidden && hideSoon());
    // caret inside a link shows the card too, like Docs
    const caretCard = () => {
      const node = getSelection().anchorNode;
      const a = node && (node.nodeType === 1 ? node : node.parentElement).closest(".ProseMirror a");
      if (a) show(a);
      else if (!card.contains(document.activeElement) && !card.matches(":hover")) hide();
    };
    editor.on("caretChange", caretCard);

    card.addEventListener("click", async (e) => {
      const act = e.target.closest("button[data-act]")?.dataset.act;
      if (!act || !current) return;
      const { from, to, mark } = range(current);
      if (act === "copy") {
        await navigator.clipboard.writeText(current.getAttribute("href") || "");
        e.target.closest("button").dataset.tip = "Copied";
      } else if (act === "remove") {
        view.dispatch(view.state.tr.removeMark(from, to, linkType));
        hide();
        view.focus();
      } else if (act === "apply") {
        applyEdit();
      } else if (act === "edit") {
        editForm.hidden = false;
        editInput.value = current.getAttribute("href") || "";
        editInput.select();
      }
    });
    // not a <form>: it sits inside the admin form, and Enter must not submit the club page
    const applyEdit = () => {
      if (!current || !editInput.value.trim()) return;
      const { from, to, mark } = range(current);
      view.dispatch(view.state.tr.removeMark(from, to, linkType).addMark(from, to, linkType.create({ ...mark?.attrs, linkUrl: editInput.value.trim() })));
      hide();
      view.focus();
    };
    editInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        applyEdit();
      } else if (e.key === "Escape") hide();
    });

    // a new table starts the cursor in its first cell, like Docs (Toast leaves it in the last one)
    host.addEventListener("mouseup", (e) => {
      if (!e.target.closest(".toastui-editor-popup-add-table")) return;
      setTimeout(() => {
        const { state } = view;
        const $from = state.selection.$from;
        for (let d = $from.depth; d > 0; d--) {
          if ($from.node(d).type.name !== "table") continue;
          let first = null;
          $from.node(d).descendants((n, pos) => {
            if (first === null && n.isTextblock) first = pos;
            return first === null;
          });
          const TextSelection = state.selection.constructor;
          view.dispatch(state.tr.setSelection(TextSelection.create(state.doc, $from.start(d) + first + 1)));
          view.focus();
          return;
        }
      }, 50);
    });
  }
});
