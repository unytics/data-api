import { load } from './mosaic.js';

const mosaicBaseURL = 'https://idl.uw.edu/mosaic/';

const selector = document.querySelector('#selector');
const view = document.querySelector('#view');
const yaml = document.querySelector('#yaml');

async function listYamlSpecs() {
  const regexp = /<li><a[^>]*>([^<]*)</g;
  const yamlSpecsHTML = await fetch('/specs/').then(res => res.text());
  return [...yamlSpecsHTML.matchAll(regexp)].map(([, name]) => name);
}

const local_yaml_examples = await listYamlSpecs();
const mosaic_yaml_examples = ["aeromagnetic-survey", "airline-travelers", "athletes", "athlete-birth-waffle", "athlete-height", "axes", "bias", "contours", "crossfilter", "density-groups", "density1d", "density2d", "driving-shifts", "earthquakes-feed", "earthquakes-globe", "facet-interval", "flights-200k", "flights-10m", "flights-density", "flights-hexbin", "gaia", "line-density", "line", "line-multi-series", "linear-regression", "linear-regression-10m", "legends", "mark-types", "moving-average", "normalize", "nyc-taxi-rides", "observable-latency", "overview-detail", "pan-zoom", "population-arrows", "presidential-opinion", "protein-design", "region-tests", "seattle-temp", "sorted-bars", "splom", "symbols", "table", "unemployment", "us-county-map", "us-state-map", "voronoi", "walmart-openings", "weather", "wind-map", "wnba-shots"];
selector.innerHTML = (
  local_yaml_examples.map( (yaml) => `<option base-url="${window.location.origin}/" value="specs/${yaml}">${yaml.replace('.yaml', '')}</option>` ) +
  mosaic_yaml_examples.map( (yaml) => `<option base-url="${mosaicBaseURL}" value="specs/yaml/${yaml}.yaml">${yaml}</option>` )
);

async function loadDashboard() {
  const selectedElement = selector.item(selector.selectedIndex);
  const baseURL = selectedElement.getAttribute('base-url');
  const specURL = `${baseURL}${selector.value}`;
  console.log('baseURL', baseURL);
  console.log('specURL', specURL);
  await load(specURL, baseURL, view, yaml);
}

selector.addEventListener('change', loadDashboard);

loadDashboard();