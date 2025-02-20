<template>
  <div class="dflex text-right" v-if="showOptions">
    <div class="btn-group mr-2" role="group">
      <button
        :class="graphStyle == 'elk-stress' ? 'btn btn-default active' : 'btn btn-default'"
        @click="graphStyle = 'elk-stress'"
      >
        stress
      </button>
      <button
        :class="graphStyle == 'cola' ? 'btn btn-default active' : 'btn btn-default'"
        @click="graphStyle = 'cola'"
      >
        force
      </button>
      <button
        :class="graphStyle == 'elk-layered-down' ? 'btn btn-default active' : 'btn btn-default'"
        @click="graphStyle = 'elk-layered-down'"
      >
        horizontal
      </button>
      <button
        :class="graphStyle == 'elk-layered-right' ? 'btn btn-default active' : 'btn btn-default'"
        @click="graphStyle = 'elk-layered-right'"
      >
        vertical
      </button>
    </div>
  </div>
  <div id="cy" v-bind="$attrs" />
</template>

<script>
// import { getItemGraph } from "@/server_fetch_utils.js";
import { itemTypes } from "@/resources.js";
import cytoscape from "cytoscape";
import dagre from "cytoscape-dagre";
import cola from "cytoscape-cola";
import elk from "cytoscape-elk";

cytoscape.use(dagre);
cytoscape.use(cola);
cytoscape.use(elk);

const layoutOptions = {
  "elk-layered-down": {
    name: "elk",
    elk: {
      algorithm: "layered",
      "elk.direction": "DOWN",
    },
  },
  "elk-layered-right": {
    name: "elk",
    elk: {
      algorithm: "layered",
      "elk.direction": "RIGHT",
    },
  },
  "elk-stress": {
    name: "elk",
    elk: {
      algorithm: "stress",
    },
  },
  cola: {
    name: "cola",
    animate: "true",
  },
};

export default {
  props: {
    graphData: Object,
    defaultGraphStyle: {
      type: String,
      default: "elk-stress",
    },
    showOptions: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      graphStyle: this.defaultGraphStyle,
    };
  },
  methods: {
    generateCyNetworkPlot() {
      if (!this.graphData) {
        return;
      }
      var cy = cytoscape({
        container: document.getElementById("cy"),
        elements: this.graphData,
        userPanningEnabled: true,
        minZoom: 0.5,
        maxZoom: 1,
        animatedZooming: false,
        userZoomingEnabled: true,
        wheelSensitivity: 0.2,
        boxSelectionEnabled: false,
        style: [
          {
            selector: "node",
            style: {
              "background-color": "#11479e",
              label: "data(id)",
            },
          },

          {
            selector: "edge",
            style: {
              width: 4,
              "target-arrow-shape": "triangle",
              "line-color": "#9dbaea",
              "target-arrow-color": "#9dbaea",
              "curve-style": "bezier",
            },
          },
        ],
        layout: layoutOptions[this.graphStyle],
      });

      // set colors of each of the nodes by type
      cy.nodes().each(function (element) {
        element.style(
          "background-color",
          element.data("special") == 1
            ? itemTypes[element.data("type")].lightColor
            : itemTypes[element.data("type")].navbarColor
        );
        element.style("border-width", element.data("special") == 1 ? 2 : 0);
        element.style("border-color", "grey");
        element.style("shape"), element.data("shape") == "triangle" ? "triangle" : "ellipse";
      });

      // tapdragover and tapdragout are mouseover and mouseout events
      // that also work with touch screens
      cy.on("tapdragover", "node", function (evt) {
        var node = evt.target;
        node.style("opacity", 0.8);
        node.style("border-width", 3);
        node.style("border-color", "black");
      });
      cy.on("tapdragout", "node", function (evt) {
        var node = evt.target;
        node.style("opacity", 1);
        node.style("border-width", node.data("special") == 1 ? 2 : 0);
        node.style("border-color", "grey");
      });

      cy.on("click", "node", function (evt) {
        var node = evt.target;
        if (node.data("type") == "collections") {
          window.open(`/collections/${node.data("id").replace("Collection: ", "")}`, "_blank");
        } else {
          window.open(`/edit/${node.data("id")}`, "_blank");
        }
      });
    },
  },
  watch: {
    graphData() {
      this.generateCyNetworkPlot();
    },
    graphStyle() {
      console.log("graphStyle changed");
      this.generateCyNetworkPlot();
    },
  },
  async mounted() {
    this.generateCyNetworkPlot();
  },
};
</script>

<style scoped>
#flex-container {
  flex-flow: column;
}

#cy {
  width: 100%;
  height: 800px;
  /* display: block;*/
}
</style>
