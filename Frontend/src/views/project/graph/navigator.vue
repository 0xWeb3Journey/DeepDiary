<template>
  <div class="GraphNavigator-container">
    <!-- <h2>interactiveGraph</h2> -->
    <div style="height: 100%">
      <div id="GraphNavigator"></div>
    </div>
  </div>
</template>

<script>
  import '/public/static/interactive-graph-0.1.0/interactive-graph.min.css'
  import '/public/static/jquery-3.2.1/jquery-3.2.1.min.js'
  import '/public/static/jquery-3.2.1/jquery-ui.css'
  import '/public/static/jquery-3.2.1/jquery-ui.js'
  import '/public/static/font-awesome-4.7.0/css/font-awesome.min.css'
  import igraph from '/public/static/interactive-graph-0.1.0/interactive-graph.min.js'
  import { baseURL } from '@/config'
  export default {
    name: 'GraphNavigator',
    components: {},
    props: {},
    data() {
      return {
        str: {
          categories: {
            person: '人物',
            organization: '机构',
            location: '地点',
          },
          data: {
            nodes: [
              {
                id: '1',
                label: 'bluejoe',
                value: 150,
                image: 'https://bluejoe2008.github.io/bluejoe3.png',
                categories: ['person'],
                info: 'demo1',
              },
              {
                id: '2',
                label: 'CNIC',
                value: 30,
                image: 'https://bluejoe2008.github.io/cas.jpg',
                categories: ['organization'],
                info: 'demo2',
              },
              {
                id: '3',
                label: 'beijing',
                value: 20,
                image: 'https://bluejoe2008.github.io/beijing.jpg',
                categories: ['location'],
                info: 'demo3',
              },
            ],
            edges: [
              { from: '1', to: '2', label: 'work for' },
              { from: '1', to: '3', label: 'live in' },
            ],
          },
          translator: {
            nodes: function (node) {
              console.log('here is the translator')
              //set description
              if (node.description === undefined) {
                var description = '<p align=left>'
                description += "<img src='" + node.image + "' width=350/><br>"
                description += '<b>' + node.label + '</b>' + '[' + node.id + ']'
                description += '</p>'
                node.description = description
              }
            },
          },
        },
      }
    },
    computed: {},
    watch: {},
    created() {},
    mounted() {
      igraph.i18n.setLanguage('chs')
      var url = baseURL + '/api/img/graph/'
      console.log('url:', url)
      var appNavigator = new igraph.GraphNavigator(
        document.getElementById('GraphNavigator'),
        'LIGHT'
      )

      // appNavigator.connectService(
      //   igraph.LocalGraph.fromGsonString(JSON.stringify(this.str))
      // )
      appNavigator.loadGson(
        // 'https://www.deep-diary.com/api/faces/test/',
        // 'http://127.0.0.1:8000/api/img/graph/',
        url,
        {
          onGetNodeDescription: function (node) {
            console.log(node)
            var description = `
              <div style="max-width: 200px; word-wrap: break-word;">
                ${
                  node.image !== undefined
                    ? `<img src="${node.image}" width="200" /><br>`
                    : ''
                }
                <b>${node.label}</b> [${node.id}]
                ${
                  node.caption !== undefined
                    ? `<p align="left">Caption: ${node.caption}</p>`
                    : ''
                }
                ${
                  node.desc !== undefined
                    ? `<p align="left">Desc: ${node.desc}</p>`
                    : ''
                }
                ${
                  node.tags !== undefined
                    ? `<p align="left">Tag: ${node.tags}</p>`
                    : ''
                }
              </div>
            `

            return description
          },
        },
        function () {}
      )
      // Not allowed to load local resource, but the http url, which si through get method
    },
    methods: {},
  }
</script>

<style lang="css" scoped>
  #GraphNavigator {
    height: 1000px;
    border: 1px solid lightgray;
  }
</style>
