using UnityEngine;

[CreateAssetMenu(menuName = "Game/Item")]
public class ItemData : ScriptableObject
{
    public string itemName;
    [TextArea] public string description;
    public Sprite icon;
    public Color color = Color.white;
    public int width = 1;
    public int height = 1;
    public float healAmount;
    public float batteryAmount;
    public bool isMagazine;
    public int magazineRounds = 12;
}