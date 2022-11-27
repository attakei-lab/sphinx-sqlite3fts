class SearchEngine {
  SQLITE_BASE = "https://unpkg.com/@antonz/sql.js@3.38.2/dist";
  SEARCH_QUERY = `
    SELECT d.page AS page, s.ref AS ref, d.title AS doc, s.root AS root, s.title AS title
    FROM section AS s, document AS d, content(:keyword) AS c
    WHERE s.document_id = d.id AND c.rowid = s.id;
    ORDER BY bm25(c)
  `;

  constructor() {
    this.isReady = false;
    this.db = null;
    this.query = null;
    this.script = document.createElement("script");
    this.script.src = `${this.SQLITE_BASE}/sql-wasm.js`;
    this.script.addEventListener("load", () => this.onLoadSQLjs());
    document.body.appendChild(this.script);
    this.renderSearchRunning();
  }

  async onLoadSQLjs() {
    const sqlPromise = initSqlJs({
      locateFile: file => `${ this.SQLITE_BASE }/${file}`,
    });
    const dataPromise = fetch(`${DOCUMENTATION_OPTIONS.URL_ROOT}db.sqlite`).then(res => res.arrayBuffer());
    const [SQL, buf] = await Promise.all([sqlPromise, dataPromise]);
    this.db = new SQL.Database(new Uint8Array(buf));
    this.isReady = true;
    if (this.query) {
      this.executeSearch(this.query);
      this.query = null
    }
  }

  executeSearch(query) {
    // TODO: Flush current result
    console.log(`Start search from database: ${query}`);
    const stmt = this.db.prepare(this.SEARCH_QUERY);
    stmt.bind([query]);
    // Post search
    const result = {
      query,
      documents: {},
    };
    while( stmt.step() ) {
      const rslt = stmt.getAsObject();
      if (!result.documents[rslt.page]) {
        result.documents[rslt.page] = {
          root: null,
          sections: [],
        }
      }
      if (rslt.root) {
        result.documents[rslt.page].root = rslt;
      } else {
        result.documents[rslt.page].sections.push(rslt);
      }
    }
    console.debug(result);
    // TODO: Render result
    this.renderSearchResult(result);
  }

  renderSearchRunning() {
    const searchResults = document.getElementById("search-results");
    const titleElement = document.createElement("h1");
    titleElement.setAttribute("class", "search-title");
    titleElement.innerText = _("Searching");
    searchResults.appendChild(titleElement);
    const summaryElement = document.createElement("p");
    summaryElement.setAttribute("class", "search-summary");
    searchResults.appendChild(summaryElement);
    const listElement = document.createElement("ul");
    listElement.setAttribute("class", "search-list");
    searchResults.appendChild(listElement);
  }

  renderSearchResult(result) {
    const countDocs = Object.keys(result.documents).length;
    const searchResults = document.getElementById("search-results");
    searchResults.querySelector("h1.search-title").innerText = _("Search Results");
    if (countDocs === 0) {
      searchResults.querySelector("p.search-summary").innerText = _(
        "Your search did not match any documents. Please make sure that all words are spelled correctly and that you've selected enough categories."
      );
      return;
    }
    console.log(`Fetch ${countDocs} documents`);
    searchResults.querySelector("p.search-summary").innerText = _(`Search finished, found ${countDocs} page(s) matching the search query.`);
    Object.values(result.documents).forEach(doc => {
      const elm = document.createElement("li");
      const root = doc.root || doc.sections[0];
      const url = new URL(`${DOCUMENTATION_OPTIONS.URL_ROOT}${root.page}`, location);
      url.searchParams.set("highlight", result.query.split()[0]);
      elm.innerHTML = `<a href="${url.href}">${root.doc}</a>`;
      searchResults.querySelector("ul.search-list").appendChild(elm);
    });
  }
}


const Search = {
  engine: new SearchEngine(),

  init() {
    const query = new URLSearchParams(window.location.search).get("q");
    document
      .querySelectorAll('input[name="q"]')
      .forEach((el) => (el.value = query));
    if (!query) {
      return;
    }
    if (Search.engine.isReady) {
      console.debug("Start search");
      Search.engine.executeSearch(query);
    } else {
      console.debug("Wait search");
      Search.engine.query = query;
    }
  },

  loadIndex() {},
  setIndex() {},
}


_ready(Search.init);
