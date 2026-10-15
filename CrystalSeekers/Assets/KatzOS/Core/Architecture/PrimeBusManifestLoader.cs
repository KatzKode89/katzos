using System;
using System.IO;
using UnityEngine;

public class PrimeBusManifestLoader : MonoBehaviour
{
    [System.Serializable]
    public class KosManifest
    {
        public string project;
        public string type;
        public string prime_bus;
        public bool vram_lock;
        public string author;
    }

    void Start()
    {
        string path = Path.Combine(Application.dataPath, "KatzOS/Core/Architecture/kos_manifest.json");
        if (File.Exists(path))
        {
            string json = File.ReadAllText(path);
            KosManifest manifest = JsonUtility.FromJson<KosManifest>(json);
            Debug.Log($"[PRIMEBUS] Loaded Sovereign Module: {manifest.project} | Bus: {manifest.prime_bus}");
        }
        else
        {
            Debug.LogWarning("[PRIMEBUS] Manifest not detected in pipeline target.");
        }
    }
}
