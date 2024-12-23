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
  // const selectedElement = selector.item(selector.selectedIndex);
  // const baseURL = selectedElement.getAttribute('base-url');
  // const specURL = `${baseURL}${selector.value}`;
  // const specContent = await fetch(specURL).then(res => res.text())
  // console.log('baseURL', baseURL);
  // console.log('specURL', specURL);
  const spec = editor.getValue();
  const baseURL = `${window.location.origin}/`;
  await load(spec, baseURL, view, yaml);
}

selector.addEventListener('change', loadDashboard);










var editor = monaco.editor.create(document.getElementById('editor'), {
  value: `
meta:
  title: Sorted Bars
  description: >
    Sort and limit an aggregate bar chart of gold medals by country.
data:
  costs_by_user_day: { file: data/costs_by_user_day_000000000000.parquet }
  top_users: >
    select user from costs_by_user_day group by user order by sum(cost) desc limit 10
params:
  # user: {select: 'single'}
  domain: [sun, fog, drizzle, rain, snow]
  colors: ['#e7ba52', '#a7a7a7', '#aec7e8', '#1f77b4', '#9467bd']
vconcat:
# - input: menu
#   label: Sport
#   as: $query
#   from: costs_by_user_day
#   column: sport
#   value: aquatics
# - vspace: 10
#  - input: search
#    label: User
#    # filterBy: $category
#    as: $user
#    from: costs_by_user_day
#    column: user
#    type: contains
#  - plot:
#    - mark: ruleY
#      data: [0]
#    - mark: lineY
#      data: { from: costs_by_user_day, optimize: false, filterBy: $user }
#      x: date
#      y: { sum: cost }
#      z: user
#      stroke: steelblue
#      strokeOpacity: 0.9
#      curve: monotone-x
#    - { select: nearestX, channels: ['z'], as: $user }
#    - { select: highlight, by: $user }
#    - mark: dot
#      data: { from: costs_by_user_day }
#      x: date
#      y: { sum: cost }
#      z: user
#      r: 2
#      fill: currentColor
#      select: nearestX
#    - mark: text
#      data: { from: costs_by_user_day }
#      x: date
#      y: user
#      text: user
#      fill: currentColor
#      dy: -8
#      select: nearestX
  # - plot:
  #   - mark: lineY
  #     data: { from: costs_by_user_day, optimize: false, filterBy: $user }
  #     x: date
  #     y: { sum: cost }
  #     stroke: user
  #     strokeOpacity: 0.9
  #     curve: monotone-x
  #   - select: intervalX
  #     as: $range
  #     brush: { fill: none, stroke: '#888' }
  #   - select: highlight
  #     by: $range
  #     fill: '#ccc'
  #     fillOpacity: 0.2
  #   - legend: color
  #     as: $user
  #     columns: 1
  - plot:
    - mark: barX
      data: { from: costs_by_user_day, filterBy: $user }
      x: { sum: cost }
      y: user
      fill: steelblue
      sort: { y: -x, limit: 10 }
    - select: toggleY
      as: $user
    - select: highlight
      by: $user
    xLabel: Gold Medals
    yLabel: Nationality
    yLabelAnchor: top
    marginTop: 15
  - input: table
    from: costs_by_user_day
    filterBy: $user
height: 300
          `,
  language: 'yaml',
          theme: "vs-dark",
          fontSize: 12,
          minimap: { enabled: false },
          // automaticLayout: true,
});

const runButton = document.getElementById('run');
runButton.addEventListener('click', loadDashboard);

loadDashboard();
