using System;
using System.IO;
using UnityEngine;

public class Sector09PuzzleController : MonoBehaviour
{
    [Header("Sector-09 Parameters")]
    public float requiredFrequency = 135.0f;
    public bool puzzleSolved = false;

    void Start()
    {
        LoadChamberData();
    }

    void LoadChamberData()
    {
        string path = Path.Combine(Application.dataPath, "KatzOS/Core/Architecture/sector09_chamber.json");
        if (File.Exists(path))
        {
            string json = File.ReadAllText(path);
            Debug.Log($"[SECTOR-09] Loaded Chamber Logic. Target Resonance: {requiredFrequency} Hz");
        }
    }

    public void VerifyResonanceFrequency(float currentFrequency)
    {
        if (Mathf.Abs(currentFrequency - requiredFrequency) < 0.1f)
        {
            puzzleSolved = true;
            Debug.Log("[SECTOR-09 SUCCESS] Frequency match verified. Labyrinth door unlocked.");
        }
    }
}
