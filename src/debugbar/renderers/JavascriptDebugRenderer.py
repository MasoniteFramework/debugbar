import os
from ..helpers.script import script
from ..helpers.css import css


class JavascriptDebugRenderer:
    def __init__(self, debugger):
        self.debugger = debugger

    def render(self, meta=None):
        data = {}
        if meta is None:
            meta = []
        for name, collector in self.debugger.collectors.items():
            data.update({collector.name: collector.collect()})

        alpinejs = script(__file__, "../resources/js/alpine.min.js")
        persistjs = script(__file__, "../resources/js/alpine.persist.min.js")
        highlightjs = script(__file__, "../resources/js/highlight.min.js")
        tailwindcss = css(__file__, "../resources/css/tailwind.min.css")

        return (
            tailwindcss
            + """
            <style>
            #debugbar .resize-handle {
                height: 6px;
                margin-top: -4px;
                width: 100%;
                background: none;
                cursor: ns-resize;
            }
            .alternate-white:nth-child(odd) {
                background-color: white
            }
            .alternate-gray:nth-child(even) {
                background-color: #e2e8f0
            }
            </style>
            <div id="debugbar" class="fixed inset-x bottom-0 h-72 bg-white w-full overflow-hidden" x-data="bar" style="z-index: 10000">
                <div x-ref="dragcapture" class="drag-capture"></div>
                <div class="resize-handle" @mousedown="resizeBar" @mouseup="mouseup"></div>
                <nav class="relative z-0 flex justify-between pr-2 items-center border-t border-gray-300 bg-gray-100" aria-label="Tabs">
                    <!-- tabs -->
                    <div class="flex divide-x divide-gray-300 items-center">
                        <template x-for="tab in tabs">
                        <a
                            @click="setTab(tab.label)"
                            class="text-gray-700 cursor-pointer flex-shrink-0 group relative flex-1 px-2 py-1.5 text-sm font-base text-center hover:bg-gray-50 focus:z-10"
                        >
                            <div class="flex items-center space-x-1 justify-between">
                                <span x-text="tab.label"></span>
                                <span x-text="tab.count" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-200 text-red-800"></span>
                            </div>
                            <span
                                aria-hidden="true"
                                class="absolute inset-x-0 bottom-0 h-0.5"
                                :class="currentTab == tab.label ? 'bg-red-500' : 'bg-transparent'"
                            ></span>
                        </a>
                        </template>
                    </div>
                    <div class="flex items-center space-x-1">
                        <div>
                            <select x-model="currentRequest" @change="getRequestData(currentRequest.request_id)" class="
                                    form-select
                                    block w-full pl-3 pr-10
                                    h-6
                                    appearance-none
                                    text-sm
                                    font-normal
                                    text-gray-700
                                    bg-white bg-clip-padding bg-no-repeat
                                    border border-solid border-gray-300
                                    rounded
                                    transition
                                    ease-in-out
                                    m-0
                                    focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none">
                                <template x-for="request in requests" :key="request.request_id">
                                <option :value="request.request_id" x-text="request.request_url"></option>
                                </template>
                            </select>
                        </div>
                        <!-- actions -->
                        <button
                            x-show="!minimized"
                            @click="minimizeBar"
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-500 hover:text-gray-600" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M15.707 4.293a1 1 0 010 1.414l-5 5a1 1 0 01-1.414 0l-5-5a1 1 0 011.414-1.414L10 8.586l4.293-4.293a1 1 0 011.414 0zm0 6a1 1 0 010 1.414l-5 5a1 1 0 01-1.414 0l-5-5a1 1 0 111.414-1.414L10 14.586l4.293-4.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                            </svg>
                        </button>
                        <button
                            x-show="minimized"
                            @click="reOpenBar"
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-500 hover:text-gray-600" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M4.293 15.707a1 1 0 010-1.414l5-5a1 1 0 011.414 0l5 5a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414 0zm0-6a1 1 0 010-1.414l5-5a1 1 0 011.414 0l5 5a1 1 0 01-1.414 1.414L10 5.414 5.707 9.707a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                            </svg>
                        </button>
                        <button
                            @click="closeBar"
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-500 hover:text-gray-600" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                            </svg>
                        </button>
                    </div>
                </nav>

                <!-- content -->
                <div class="h-full" x-show="!minimized">
                    <!-- header -->
                    <div class="border border-b border-gray-300 p-1">
                        <p x-text="currentContent.description" class="text-sm text-gray-500"></p>
                    </div>
                    <!-- content container-->
                    <div class="h-full overflow-y-auto">
                        <div x-html="currentContent.html"></div>
                    </div>
                </div>
            </div>

            <script>
                document.addEventListener("alpine:init", () => {
                    Alpine.data("bar", function () {
                    return {
                        rawData: {},
                        tabs: [],
                        content: [],
                        currentTab: this.$persist("Messages"),
                        currentContent: {},
                        requests: [],
                        currentRequest: "",
                        loading: true,
                        // resize
                        orig_h: null,
                        pos_y: null,
                        initHeight: this.$persist(288), // h-72
                        // minimizing, closing
                        displayed: true,
                        minimized: this.$persist(false),
                        init() {
                            const alpineInstance = this
                            const _debugbarOriginalAjax = window.XMLHttpRequest.prototype.send
                            const _debugbarOriginalFetch = window.fetch

                            // intercept basic AJAX request to populate request select box
                            const interceptAjax = function() {
                                this.addEventListener("loadend", function() {
                                    alpineInstance.getRequestData(alpineInstance.currentRequest)
                                }, false)
                                return _debugbarOriginalAjax.apply(this, [].slice.call(arguments))
                            }
                            window.XMLHttpRequest.prototype.send = interceptAjax

                            // intercept AJAX request using fetch() to populate request select box
                            const interceptFetch = function() {
                                const url = arguments[0]
                                return _debugbarOriginalFetch.apply(this, arguments)
                                    .then((res) => {
                                        // intercept only requests which are not debugbar endpoints
                                        if (!url.startsWith("/_debugbar/")) {
                                            alpineInstance.getRequestData(alpineInstance.currentRequest)
                                        }
                                        return res;
                                    })
                            }
                            window.fetch = interceptFetch

                            // define how debugbar be displayed
                            this.setHeight(this.initHeight)
                            if (this.minimized) {
                                this.minimizeBar()
                            }
                            // load current HTML request
                            this.getRequestData()
                        },
                        async getRequestData(id = null) {
                            this.loading = true
                            if (this.currentRequest) {
                                this.rawData = await (await fetch(`/_debugbar/${this.currentRequest}/`)).json();
                            } else {
                                this.rawData = await (await fetch("/_debugbar/")).json()
                            }

                            this.content = this.rawData.data
                            this.requests = this.rawData.requests
                            this.tabs = []
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
                            hljs.highlightAll()
                        },
                        getTabContent(tab) {
                            return this.content[tab]
                        },
                        // resize handler
                        setHeight(height) {
                            this.$root.style.height = `${height}px`
                            this.initHeight = height
                        },
                        resizeBar(e) {
                            this.orig_h = this.$root.clientHeight
                            this.pos_y = e.pageY
                            this.callback = (event) => this.mousemove(event)
                            document.body.addEventListener("mousemove", this.callback)
                            this.$refs.dragcapture.display = "block";
                            e.preventDefault()
                        },
                        mousemove(e) {
                            var h = this.orig_h + (this.pos_y - e.pageY)
                            this.setHeight(h)
                        },
                        mouseup(e) {
                            document.body.removeEventListener("mousemove", this.callback)
                        },
                        // closing
                        closeBar () {
                            this.displayed = false
                            this.$root.style.display = "none"
                        },
                        minimizeBar () {
                            this.minimized = true
                            this.$root.style.height = "35px"
                        },
                        reOpenBar () {
                            this.minimized = false
                            this.setHeight(this.initHeight)
                        }
                    }
                    })
                })
            </script>
        """
            + persistjs
            + alpinejs
            + highlightjs
        )
