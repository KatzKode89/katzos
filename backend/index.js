import express from "express";
import cors from "cors";

const app = express();
app.use(cors());
app.use(express.json());

// --- In-memory demo data (v0) ---

const devices = [];

const items = [
  {
    id: "tmdb:12345:S01E01",
    type: "episode",
    title: "Example Show – S01E01",
    season: 1,
    episode: 1,
    year: 2024,
    in_watchlist: true,
    watched: false,
    progress: 812,
    apps: ["BeeTV", "FilmPlus"],
    has_torrents: true
  },
  {
    id: "tmdb:99999",
    type: "movie",
    title: "Example Movie",
    year: 2023,
    in_watchlist: false,
    watched: false,
    progress: 0,
    apps: ["FilmPlus"],
    has_torrents: false
  }
];

const sources = [
  {
    id: "src_1",
    item_id: "tmdb:12345:S01E01",
    source_app: "FilmPlus",
    provider: "VidCloud",
    quality: "1080p",
    type: "m3u8",
    url: "https://example.com/stream1.m3u8",
    language: "EN",
    size: "1.2GB",
    last_seen: Date.now()
  },
  {
    id: "src_2",
    item_id: "tmdb:12345:S01E01",
    source_app: "BeeTV",
    provider: "TorrentProvider",
    quality: "1080p",
    type: "torrent",
    url: "magnet:?xt=urn:btih:EXAMPLE",
    language: "EN",
    size: "1.3GB",
    last_seen: Date.now()
  }
];

const progress = [
  {
    item_id: "tmdb:12345:S01E01",
    title: "Example Show – S01E01",
    progress: 812
  }
];

// --- KOS.Devices ---

app.post("/kos/devices/register", (req, res) => {
  const { device_id, name, type, capabilities } = req.body;
  if (!device_id) return res.status(400).json({ error: "device_id required" });

  let device = devices.find(d => d.id === device_id);
  if (!device) {
    device = {
      id: device_id,
      name: name || device_id,
      type: type || "unknown",
      capabilities: capabilities || [],
      last_seen: Date.now()
    };
    devices.push(device);
  } else {
    device.last_seen = Date.now();
  }

  res.json({ success: true, device });
});

app.get("/kos/devices/list", (req, res) => {
  res.json(devices);
});

// --- KOS.Media: progress ---

app.get("/kos/media/progress", (req, res) => {
  const { device_id } = req.query;
  res.json(progress);
});

// --- KOS.Media: search ---

app.get("/kos/media/search", (req, res) => {
  const { q } = req.query;
  if (!q) return res.json(items);

  const query = q.toLowerCase();
  const results = items.filter(i => i.title.toLowerCase().includes(query));
  res.json(results);
});

// --- KOS.Media: item details ---

app.get("/kos/media/item", (req, res) => {
  const { id } = req.query;
  const item = items.find(i => i.id === id);
  if (!item) return res.status(404).json({ error: "not found" });

  const itemSources = sources.filter(s => s.item_id === id);
  res.json({ item, sources: itemSources });
});

// --- KOS.Media: best source ---

app.get("/kos/media/sources/best", (req, res) => {
  const { item_id, allow_torrents } = req.query;
  const allowTorrents = allow_torrents === "true";

  let candidates = sources.filter(s => s.item_id === item_id);
  if (!allowTorrents) {
    candidates = candidates.filter(s => s.type !== "torrent");
  }

  if (candidates.length === 0) {
    return res.status(404).json({ error: "no sources" });
  }

  const best = candidates[0];
  res.json(best);
});

// --- KOS.Media: torrent sources ---

app.get("/kos/media/sources/torrent", (req, res) => {
  const { item_id } = req.query;
  const torrents = sources.filter(
    s => s.item_id === item_id && s.type === "torrent"
  );
  res.json(torrents);
});

// --- KOS.AI: stub ---

app.post("/kos/ai", (req, res) => {
  const { text, device_id } = req.body;
  res.json({
    reply: `KatzAI (stub): you said "${text}" on device "${device_id}".`,
    actions: []
  });
});

// --- Start server ---

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`KatzOS v0 running on port ${port}`);
});
