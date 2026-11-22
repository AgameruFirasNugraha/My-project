using Unity.Cinemachine;
using UnityEngine;

public class PlayerSpawner : MonoBehaviour
{
    [SerializeField] private GameObject playerSystemPrefab;

    void Awake()
    {
        GameObject player;

        if (PersistentPlayer.Instance != null)
        {
            player = PersistentPlayer.Instance.gameObject;
        }
        else
        {
            player = Instantiate(playerSystemPrefab);
        }

        MoveTo(player, transform.position);
    }

    void MoveTo(GameObject player, Vector3 position)
    {
        CinemachineCamera vcam = player.GetComponentInChildren<CinemachineCamera>(true);
        bool wasActive = vcam != null && vcam.gameObject.activeSelf;

        if (vcam != null) { vcam.gameObject.SetActive(false); }

        player.transform.position = position;

        foreach (Rigidbody2D body in player.GetComponentsInChildren<Rigidbody2D>())
        {
            body.linearVelocity = Vector2.zero;
        }

        Physics2D.SyncTransforms();

        if (vcam != null && wasActive) { vcam.gameObject.SetActive(true); }
    }
}