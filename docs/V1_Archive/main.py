import os
from agents.a1_interaction import AgentA1
from agents.a2_research import AgentA2
from agents.a3_redactor import AgentA3
from agents.a5_supervisor import AgentA5
from agents.a4_delivery import AgentA4

def main():
    print("🚀 Lancement du Réseau Hermes Newsletter")

    # 1. Interaction (A1)
    a1 = AgentA1()
    a1.collect_info()

    # 2. Recherche (A2)
    a2 = AgentA2(model_name="llama3.1:8b")
    a2.perform_research()

    # 3. Rédaction (A3)
    a3 = AgentA3(model_name="llama3.1:8b")
    a3.write_newsletter()

    # 4. Supervision (A5)
    a5 = AgentA5(model_name="llama3.1:8b")
    is_valid = a5.supervise()

    if is_valid:
        # 5. Livraison (A4)
        a4 = AgentA4()
        a4.deliver()
        print("\n🎉 Processus terminé avec succès !")
    else:
        print("\n⚠️ Le processus s'est arrêté car A5 a rejeté la newsletter.")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
