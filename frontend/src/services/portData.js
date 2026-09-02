// Port dataset extracted from Charter Cast backend ML categories and port constraint master datasets.

export const PORT_OPTIONS = [
  // Indian & Major Regional Origin Ports
  { value: "Paradip Port", label: "Paradip Port (East Coast India)" },
  { value: "Visakhapatnam (Vizag) Port", label: "Visakhapatnam (Vizag) Port (East Coast India)" },
  { value: "Dhamra Port", label: "Dhamra Port (East Coast India)" },
  { value: "Haldia Dock Complex (SMP Kolkata)", label: "Haldia Dock Complex (East Coast India)" },
  { value: "Chennai Port", label: "Chennai Port (East Coast India)" },
  { value: "Gangavaram Port", label: "Gangavaram Port (Andhra Pradesh)" },
  { value: "Gopalpur Port", label: "Gopalpur Port (Odisha)" },
  { value: "Kamarajar (Ennore) Port", label: "Kamarajar Port (Tamil Nadu)" },
  { value: "Karaikal Port", label: "Karaikal Port (Puducherry)" },
  { value: "Kattupalli Port", label: "Kattupalli Port (Tamil Nadu)" },
  { value: "Krishnapatnam Port", label: "Krishnapatnam Port (Andhra Pradesh)" },
  { value: "Sagar Island & Sandheads (Anchorage)", label: "Sagar Island & Sandheads (Anchorage)" },
  { value: "VOC Port (Tuticorin)", label: "VOC Port (Tuticorin)" },
  { value: "Australia", label: "Australia (Bulk Region)" },
  { value: "Indonesia", label: "Indonesia (Coal Hub)" },
  { value: "South Africa", label: "South Africa (Richards Bay)" },
  { value: "Russia", label: "Russia (Far East Ports)" },

  // Additional Global & Destination Ports
  { value: "Dhamra", label: "Dhamra Port (East Coast India)" },
  { value: "Maurer", label: "Maurer Port" },
  { value: "Iharana", label: "Iharana Port" },
  { value: "Ammassalik", label: "Ammassalik Port" },
  { value: "Boca Grande", label: "Boca Grande" },
  { value: "Bridgwater", label: "Bridgwater" },
  { value: "Bullen Baai", label: "Bullen Baai" },
  { value: "Cabo Rojo", label: "Cabo Rojo" },
  { value: "Canaport (St. John)", label: "Canaport (St. John)" },
  { value: "Cap Haitien", label: "Cap Haitien" },
  { value: "Celukan Bawang", label: "Celukan Bawang" },
  { value: "Diego Garcia", label: "Diego Garcia" },
  { value: "Hibikinada", label: "Hibikinada" },
  { value: "Ishikari Bay New Port", label: "Ishikari Bay New Port" },
  { value: "Jiddah", label: "Jiddah Port" },
  { value: "Jurong Island", label: "Jurong Island" },
  { value: "Kota Kinabalu", label: "Kota Kinabalu" },
  { value: "Lautoka Harbor", label: "Lautoka Harbor" },
  { value: "Manati", label: "Manati" },
  { value: "Nassau", label: "Nassau" },
  { value: "Pismo Beach", label: "Pismo Beach" },
  { value: "Pointe A Pitre", label: "Pointe A Pitre" },
  { value: "Port Isabel", label: "Port Isabel" },
  { value: "Porto Di Oristano", label: "Porto Di Oristano" },
  { value: "Puerto Chacabuco", label: "Puerto Chacabuco" },
  { value: "Puerto Plata", label: "Puerto Plata" },
  { value: "Rendsburg", label: "Rendsburg" },
  { value: "San Fernando Harbor", label: "San Fernando Harbor" },
  { value: "Talcahuano", label: "Talcahuano" }
];

export const ORIGIN_PORTS = PORT_OPTIONS;
export const DESTINATION_PORTS = PORT_OPTIONS;

export const COMMODITIES = [
  { value: "Coal", label: "Thermal / Steam Coal" },
  { value: "Coking Coal", label: "Coking / Metallurgical Coal" },
  { value: "Iron Ore", label: "Iron Ore Fines / Pellets" },
  { value: "Bauxite", label: "Bauxite Ore" },
  { value: "Grain", label: "Wheat / Grain" },
  { value: "Limestone", label: "Limestone / Gypsum" }
];

export const VESSEL_TYPES = [
  { value: "Handysize", label: "Handysize (10,000 - 40,000 DWT)" },
  { value: "Supramax", label: "Supramax (40,000 - 65,000 DWT)" },
  { value: "Panamax", label: "Panamax (65,000 - 85,000 DWT)" },
  { value: "Capesize", label: "Capesize (120,000 - 210,000 DWT)" }
];

