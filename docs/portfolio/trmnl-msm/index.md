# My School Menus TRMNL Plugin Integration

The My School Menus plugin for [TRMNL device](www.trmnl.com) provides a great example of the advantages that can arise when docs are treated like code.   

My School Menus provides menu information for 1,680 school districts across the country. Because the menu information is stored in an accessible format, it can be easily extracted and displayed on the TRMNL. I use this plugin to show the family what's for hot lunch everyone morning. TRMNL displays the lunch informatino on a screen next to the weather and our daily calendar. 

You can use the tool below to find the  District, School, and Menu IDs needed to configure the TRMNL My School Menus recipe: 

1. Search for your school district, then use the drop-down menu to select your school and the menu you want displayed. 
2. Copy the values and paste them into the School IDs field in the plugin settings page. 

<div id="lookup-tool">
  <div class="step">
    <label for="district-search"><strong>1. Find your district</strong></label>
    <input type="text" id="district-search" placeholder="Type to search districts..." />
    <select id="district-select" size="8" style="width:100%; display:none;"></select>
    <p id="district-id" class="id-display"></p>
  </div>

  <div class="step">
    <label for="school-select"><strong>2. Select your school</strong></label>
    <select id="school-select" disabled>
      <option value="">-- Select a district first --</option>
    </select>
    <p id="school-id" class="id-display"></p>
  </div>

  <div class="step">
    <label for="menu-select"><strong>3. Select the menu</strong></label>
    <select id="menu-select" disabled>
      <option value="">-- Select a school first --</option>
    </select>
    <p id="menu-id" class="id-display"></p>
  </div>

  <div id="results" style="display:none;">
    <h3>Copy this into TRMNL</h3>
    <div style="display:flex; gap:0.5em; align-items:stretch;">
      <textarea id="result-block" rows="1" readonly onclick="this.select()" style="flex:1;"></textarea>
      <button id="copy-btn" onclick="copyResult()" style="padding:0.4em 0.8em; cursor:pointer;">Copy</button>
    </div>
    <p id="copy-confirm" style="font-size:0.85em; color:green; display:none;">Copied!</p>
    <p style="font-size:0.85em; color:#555;">Paste into the <strong>School IDs</strong> field in TRMNL.</p>
    <p><a id="menu-link" href="#" target="_blank">View this menu on My School Menus</a></p>
  </div>

  <p id="error-msg" style="color:red; display:none;"></p>
  <p id="loading-msg" style="display:none;"><em>Loading...</em></p>
</div>

<style>
#lookup-tool {
  max-width: 500px;
}
#lookup-tool .step {
  margin-bottom: 1.5em;
}
#lookup-tool input,
#lookup-tool select {
  width: 100%;
  padding: 0.4em;
  font-size: 1em;
  box-sizing: border-box;
}
#lookup-tool .id-display {
  margin: 0.3em 0 0;
  font-size: 0.9em;
  color: #555;
}
#results {
  margin-top: 1.5em;
  padding: 1em;
  background: #f0f7ff;
  border: 1px solid #cce0ff;
  border-radius: 4px;
}
#result-block {
  width: 100%;
  font-family: monospace;
  font-size: 1em;
  padding: 0.5em;
  box-sizing: border-box;
  background: #fff;
  border: 1px solid #aac;
  resize: none;
  cursor: pointer;
}
</style>

<script>
(function() {
  const API = "https://trmnl-msm-recipe.doc-design.workers.dev";
  let allOrgs = [];

  const districtSearch = document.getElementById("district-search");
  const districtSelect = document.getElementById("district-select");
  const schoolSelect = document.getElementById("school-select");
  const menuSelect = document.getElementById("menu-select");
  const errorMsg = document.getElementById("error-msg");
  const loadingMsg = document.getElementById("loading-msg");
  const results = document.getElementById("results");

  function showError(msg) {
    errorMsg.textContent = msg;
    errorMsg.style.display = "block";
  }

  function clearError() {
    errorMsg.style.display = "none";
  }

  function showLoading(show) {
    loadingMsg.style.display = show ? "block" : "none";
  }

  // Load all districts on page load
  async function loadOrgs() {
    showLoading(true);
    try {
      const resp = await fetch(API + "/orgs");
      if (!resp.ok) throw new Error("API returned " + resp.status);
      const json = await resp.json();
      // Worker returns [{id, name}, ...]
      allOrgs = json.sort((a, b) => a.name.localeCompare(b.name));
      clearError();
    } catch (e) {
      showError("Could not load districts: " + e.message);
    }
    showLoading(false);
  }

  function filterDistricts(query) {
    const q = query.toLowerCase();
    if (!q) {
      districtSelect.style.display = "none";
      return;
    }
    const matches = allOrgs.filter(o => o.name.toLowerCase().includes(q));
    districtSelect.innerHTML = "";
    for (const org of matches.slice(0, 50)) {
      const opt = document.createElement("option");
      opt.value = org.id;
      opt.textContent = org.name;
      districtSelect.appendChild(opt);
    }
    districtSelect.style.display = matches.length ? "block" : "none";
  }

  districtSearch.addEventListener("input", function() {
    filterDistricts(this.value);
  });

  districtSelect.addEventListener("change", async function() {
    const orgId = this.value;
    const orgName = this.options[this.selectedIndex].textContent;
    districtSearch.value = orgName;
    districtSelect.style.display = "none";
    document.getElementById("district-id").textContent = "District ID: " + orgId;

    // Reset downstream
    schoolSelect.innerHTML = '<option value="">Loading...</option>';
    schoolSelect.disabled = true;
    menuSelect.innerHTML = '<option value="">-- Select a school first --</option>';
    menuSelect.disabled = true;
    results.style.display = "none";

    try {
      // Worker returns [{"School Name": id}, ...]
      const resp = await fetch(API + "/orgs/" + orgId + "/sites");
      if (!resp.ok) throw new Error("API returned " + resp.status);
      const json = await resp.json();
      schoolSelect.innerHTML = '<option value="">-- Select a school --</option>';
      for (const site of json) {
        const name = Object.keys(site)[0];
        const id = site[name];
        const opt = document.createElement("option");
        opt.value = id;
        opt.textContent = name;
        schoolSelect.appendChild(opt);
      }
      schoolSelect.disabled = false;
      clearError();
    } catch (e) {
      showError("Could not load schools: " + e.message);
    }
  });

  schoolSelect.addEventListener("change", async function() {
    const orgId = districtSelect.value;
    const siteId = this.value;
    if (!siteId) return;
    document.getElementById("school-id").textContent = "School ID: " + siteId;

    menuSelect.innerHTML = '<option value="">Loading...</option>';
    menuSelect.disabled = true;
    results.style.display = "none";

    try {
      // Worker returns [{"Menu Name": id}, ...]
      const resp = await fetch(API + "/orgs/" + orgId + "/sites/" + siteId + "/menus");
      if (!resp.ok) throw new Error("API returned " + resp.status);
      const json = await resp.json();
      menuSelect.innerHTML = '<option value="">-- Select a menu --</option>';
      for (const menu of json) {
        const name = Object.keys(menu)[0];
        const id = menu[name];
        const opt = document.createElement("option");
        opt.value = id;
        opt.textContent = name;
        menuSelect.appendChild(opt);
      }
      menuSelect.disabled = false;
      clearError();
    } catch (e) {
      showError("Could not load menus: " + e.message);
    }
  });

  menuSelect.addEventListener("change", function() {
    const menuId = this.value;
    if (!menuId) return;
    document.getElementById("menu-id").textContent = "Menu ID: " + menuId;
    const block = districtSelect.value + "," + schoolSelect.value + "," + menuId;
    document.getElementById("result-block").value = block;
    document.getElementById("menu-link").href = "https://menus.healthepro.com/organizations/" + districtSelect.value + "/sites/" + schoolSelect.value + "/menus/" + menuId;
    results.style.display = "block";
  });

  loadOrgs();
})();

function copyResult() {
  const block = document.getElementById("result-block");
  navigator.clipboard.writeText(block.value).then(function() {
    const confirm = document.getElementById("copy-confirm");
    confirm.style.display = "block";
    setTimeout(() => confirm.style.display = "none", 2000);
  });
}
</script>
