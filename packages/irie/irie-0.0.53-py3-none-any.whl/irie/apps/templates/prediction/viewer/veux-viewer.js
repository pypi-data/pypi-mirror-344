//===----------------------------------------------------------------------===//
//
//         STAIRLab -- STructural Artificial Intelligence Laboratory
//
//===----------------------------------------------------------------------===//
//
class VeuxViewer {
    #initializedTabs;
    #table;
    #url;
    #tabLinkContainer;
    #tabContentContainer;

    constructor(url, tabLinkContainer, tabContentContainer) {
      this.#url = url;
      this.#initializedTabs = [];
      this.#tabLinkContainer = tabLinkContainer;
      this.#tabContentContainer = tabContentContainer;
    }

    initTabs(tab1, tabselector) {
        this.#initializedTabs.push(tab1);

        const tabs = this.#tabLinkContainer.querySelectorAll(tabselector);

        tabs.forEach(tab => {
            tab.addEventListener('click', (e) => {
                e.preventDefault();
                this.clickTab(tab);
            });
        });
    }

    select(elem) {
        const sname =  elem.dataset.section;

        if (this.#initializedTabs.includes(sname)) {
            const tabLink = this.#tabLinkContainer.querySelector(`#${sname}-tab`);
            this.clickTab(tabLink);
            return;
        }

        this.addTab(sname);
    }

    addTab(corr) {
        const tab = `${corr}`;
    
        //
        //
        //
        const tabLink = document.createElement('a');
        tabLink.id = `${tab}-tab`;
        tabLink.classList.add("tab-link", "nav-link", "active");
        tabLink.href = "#";
        tabLink.setAttribute('data-tab', tab);
        tabLink.setAttribute('data-section', corr);
        tabLink.setAttribute('data-bs-toggle', 'tab');
        tabLink.setAttribute('role', 'tab');
        tabLink.innerHTML = `${corr} <button class="btn-close" type="button" aria-label="Close"></button>`;
        const closeButton = tabLink.querySelector('.btn-close');
        closeButton.addEventListener('click', (e) => {
            this.delTab(tabLink);
        });
        tabLink.addEventListener('click', (e) => {
            e.preventDefault(); 
            this.clickTab(tabLink);
        });
    
        const tabItem = document.createElement('li');
        tabItem.role = 'presentation';
        tabItem.classList.add('nav-item');
        tabItem.appendChild(tabLink);
        // Add to list of tabs
        this.#tabLinkContainer.appendChild(tabItem);
    
        //
        //
        //
        const tabContent = document.createElement('div');
        tabContent.classList.add('tab-content', 'mt-3', 'card-body', 'p-2');
        tabContent.id = `${tab}-content`;
        tabContent.style.display = 'block';
        this.#tabContentContainer.appendChild(tabContent);
    
        // Get the data-tab attribute to know which content to load
        const selectedTab = tabLink.getAttribute('data-tab');
    
        this.#initializedTabs.push(tab);
    
        this.clickTab(tabLink);
    
        this.fetchAndUpdateTab(selectedTab, corr);
        return tabLink;
    }

    clickTab(tabLink) {
    
        const tabs = this.#tabLinkContainer.querySelectorAll('.tab-link');
    
        // Remove 'active' class from all tabs
        tabs.forEach(t => {
            t.classList.remove('active');
        });
    
        // Add 'active' class to the clicked tab
        tabLink.classList.add('active');
    
        const tab = tabLink.getAttribute('data-tab');
        const contentDiv = this.#tabContentContainer.querySelector(`#${tab}-content`);
    
        contentDiv.style.display = 'block';
        this.#tabContentContainer.querySelectorAll(".tab-content").forEach((el) => {
            if (el.id != `${tab}-content`) {
                el.style.display = 'none';
            }
        });
    }

    delTab(tabLink) {
        const tab = tabLink.getAttribute('data-tab');
        const corr = tabLink.getAttribute('data-corridor');
        const tabContent = this.#tabContentContainer.querySelector(`#${tab}-content`);
        tabContent.remove();

        const tabItem = tabLink.parentElement;
        tabItem.remove();

        const idx = this.#initializedTabs.indexOf(tab);
        if (idx > -1) {
            this.#initializedTabs.splice(idx, 1);
        }
        this.clickTab(document.getElementById('tab1-tab'));
    }

    fetchAndUpdateTab(tab) {
        const contentDiv = this.#tabContentContainer.querySelector(`#${tab}-content`);

        // Show loading message while content is being fetched
        contentDiv.innerHTML = `
        <div class="text-center">
            <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
        `;

        let apiUrl = `${this.#url}${tab}`;
        console.log(`Fetching content from: ${apiUrl}`);

        if (true) {
            contentDiv.innerHTML = "";
            const mv = document.createElement('model-viewer');

            mv.setAttribute('camera-controls', '');
            mv.setAttribute('autoplay', '');
            mv.setAttribute('interaction-prompt', 'none');
            mv.style.width  = '100%';
            mv.style.height = '400px';

            mv.src = apiUrl;
            contentDiv.appendChild(mv);
            return;
        }
        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                // Replace the loading message with the fetched content
                // when we get it
                contentDiv.innerHTML = "";
                const mv = document.createElement('model-viewer');

                mv.setAttribute('camera-controls', '');
                mv.setAttribute('autoplay', '');
                mv.setAttribute('interaction-prompt', 'none');
                mv.style.width  = '100%';
                mv.style.height = '400px';

                // set the data-URI source
                mv.src = `data:model/gltf-binary;base64,${data.rendering}`;
                contentDiv.appendChild(mv);
            })
            .catch(error => {
                console.error('Error fetching content:', error);
                document.getElementById('tab-content').innerHTML = '<p>Error loading content.</p>';
            });
    }
}
