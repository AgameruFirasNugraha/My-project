using UnityEngine;

[CreateAssetMenu(menuName = "Game/Item")]
public class ItemData : ScriptableObject
{
    public string itemName;
    public Sprite icon;
    public Color color = Color.white;
    public float healAmount;
    public float batteryAmount;
}