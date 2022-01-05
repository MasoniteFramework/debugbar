class JavascriptDebugRenderer:

    def __init__(self, debugger):
        self.debugger = debugger

    def render(self, meta=None):
        data = {}
        if meta is None:
            meta = []
        for name, collector in self.debugger.collectors.items():
            data.update({collector.name: collector.collect()})

        return """
            <div class="fixed inset-x bottom-0 h-72 bg-white w-full overflow-auto" x-data="bar">
                <nav class="relative z-0 flex divide-x divide-gray-300 border border-y border-gray-300 bg-gray-100" aria-label="Tabs">
                    <template x-for="tab in tabs">
                    <!-- Current: "text-gray-900", Default: "text-gray-500 hover:text-gray-700" -->
                    <!-- class="text-gray-500 hover:text-gray-700 group relative min-w-0 flex-1 overflow-hidden bg-white py-4 px-4 text-sm font-medium text-center hover:bg-gray-50 focus:z-10"> -->
                    <a
                        x-on:click="setTab(tab.label)"
                        class="text-gray-700 cursor-pointer max-w-min group relative min-w-0 flex-1 overflow-hidden py-1 px-3 text-sm font-base text-center hover:bg-gray-50 focus:z-10"
                    >
                        <div class="flex items-center space-x-1 justify-between">
                            <span x-text="tab.label"></span>
                            <span x-text="tab.count" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800"></span>
                        </div>
                        <!-- <span aria-hidden="true" class="bg-red-500 absolute inset-x-0 bottom-0 h-0.5"></span> -->
                        <span aria-hidden="true"
                        class="absolute inset-x-0 bottom-0 h-0.5"
                        :class="currentTab == tab.label ? 'bg-red-500' : 'bg-transparent'"
                        ></span>
                    </a>
                    </template>
                </nav>

                <!-- content -->
                <div>
                    <!-- header -->
                    <div class="border border-b border-gray-300 p-1">
                        <p x-text="currentContent.description" class="text-sm text-gray-500"></p>
                    </div>
                    <!-- rows -->
                    <div>
                    <template x-if="!loading">
                        <div x-html="currentContent.html"></div>
                    </template>
                    </div>
                </div>
            </div>

            <script>
                document.addEventListener('alpine:init', () => {
                    Alpine.data('bar', function () {
                    return {
                        rawData: {},
                        tabs: [],
                        content: [],
                        currentTab: this.$persist("messages"),
                        currentContent: "",
                        loading: true,
                        init() {
                            // TODO: Load JSON debugbar payload of last request
                            this.getRequestData()
                        },
                        async getRequestData(id = null) {
                            //this.rawData = await (await fetch(`/_debugbar/${id}/`)).json();
                            this.rawData = await (await fetch("/_debugbar/")).json()
                            this.content = this.rawData.data
                            for (const [label, tabData] of Object.entries(this.content)) {
                                this.tabs.push({
                                    count: tabData?.count || 0,
                                    label: label
                                })
                            }
                            this.setTab(this.currentTab)
                            this.loading = false
                        },
                        setTab(tab) {
                            this.currentTab = tab
                            this.currentContent = this.getTabContent(tab)
                        },
                        getTabContent(tab) {
                            return this.content[tab]
                        }
                    }
                    })
                })
            </script>
        """