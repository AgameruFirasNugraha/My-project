using UnityEngine;

public class SurvivorAnimator : MonoBehaviour
{
    [SerializeField] private Rigidbody2D body;
    [SerializeField] private Animator bodyAnimator;
    [SerializeField] private Animator feetAnimator;

    void Update()
    {
        float speed = body.linearVelocity.magnitude;
        bodyAnimator.SetFloat("Speed", speed);
        feetAnimator.SetFloat("Speed", speed);
    }
}