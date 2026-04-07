# Quantum Computing Education Curriculum for KALI
# Focused on simple explanations and Indian research context.

CURRICULUM = {
    "topic_1": {
        "title": "What is a Qubit?",
        "explanation": """
        Imagine a regular computer bit like a light switch that can only be either **ON (1)** or **OFF (0)**. A Qubit (short for Quantum Bit) is much more advanced. It is the basic unit of information in a quantum computer, but unlike a normal bit, it can exist in multiple states at once thanks to a special property called superposition.

        Think of a spinning coin. While it's spinning, it is both heads and tails at the same time until it stops. A qubit works similarly, allowing a quantum computer to handle massive amounts of data simultaneously, rather than one by one. This makes them incredibly powerful for solving complex puzzles that regular computers would take millions of years to solve.

        To keep these qubits working, they need to be kept extremely cold—colder than outer space! This is because even a tiny bit of heat or vibration can disturb their delicate state, causing them to lose their 'quantumness' in a process called decoherence.
        """,
        "india_example": "The Indian Institute of Science (IISc) in Bengaluru is actively researching how to build stable qubits using superconducting materials, which is a key step toward India's first home-grown quantum computer.",
        "key_terms": [
            {"term": "Bit", "definition": "A basic unit of information in regular computers (0 or 1)."},
            {"term": "Qubit", "definition": "A quantum bit that can represent 0, 1, or both simultaneously."},
            {"term": "Superposition", "definition": "The ability of a quantum system to be in multiple states at the same time."},
            {"term": "Decoherence", "definition": "When a qubit loses its quantum state due to environmental interference."},
            {"term": "Cryogenics", "definition": "The study of materials at extremely low temperatures, necessary for qubit stability."}
        ],
        "quiz": [
            {"question": "What is the main difference between a bit and a qubit?", "options": ["Bits are faster", "Qubits can be 0 and 1 at once", "Bits are smaller", "Qubits don't need electricity"], "answer": 1},
            {"question": "What happens during decoherence?", "options": ["The qubit gets stronger", "The qubit loses its quantum state", "The computer restarts", "Information is saved"], "answer": 1},
            {"question": "Why do qubits need to be kept very cold?", "options": ["To save electricity", "To prevent heat from disturbing their state", "Because they are made of ice", "To increase their size"], "answer": 1}
        ],
        "challenge": {"question": "Can a qubit be measured without ending its superposition?", "options": ["Yes", "No", "Only on Tuesdays", "If it is blue"], "answer": 1},
        "fact": "Did you know? India's National Quantum Mission has a budget of over ₹6,000 crores to develop quantum technologies by 2031!"
    },
    "topic_2": {
        "title": "Quantum Gates",
        "explanation": """
        In normal computers, 'gates' are like tiny logic gates that tell electricity where to go to perform calculations (like adding two numbers). **Quantum Gates** are similar but they operate on qubits. Instead of just switching 1s and 0s, they rotate the state of the qubit, changing its probability of being 0 or 1.

        One of the most famous quantum gates is the **Hadamard Gate**. It takes a qubit and puts it into a perfect state of superposition—making it 50% likely to be 0 and 50% likely to be 1. It's like the 'start' button for quantum weirdness.

        By combining different quantum gates, we create 'Quantum Circuits' that can perform calculations that are impossible for classical computers. These gates use mathematical rotations to move the qubit around a sphere of possibilities called the Bloch Sphere.
        """,
        "india_example": "Researchers at TIFR (Tata Institute of Fundamental Research) in Mumbai are designing high-precision quantum gates that can operate with very low error rates, essential for accurate quantum computing.",
        "key_terms": [
            {"term": "Logic Gate", "definition": "A building block of a circuit that performs a specific calculation."},
            {"term": "Hadamard Gate", "definition": "A gate that creates superposition in a qubit."},
            {"term": "Rotation", "definition": "The process of changing a qubit's state mathematically."},
            {"term": "Bloch Sphere", "definition": "A visual way to represent the state of a single qubit as a point on a sphere."},
            {"term": "Error Rate", "definition": "The frequency at which a quantum gate performs an incorrect operation."}
        ],
        "quiz": [
            {"question": "What does a Hadamard Gate do?", "options": ["Turns off the computer", "Creates superposition", "Deletes data", "Speeds up the fan"], "answer": 1},
            {"question": "How do quantum gates change a qubit's state?", "options": ["By deleting it", "By rotating its probability", "By making it heavier", "By changing its color"], "answer": 1},
            {"question": "What is the 'Bloch Sphere' used for?", "options": ["Storing data", "Visualizing a qubit's state", "Cooling the computer", "Connecting to the internet"], "answer": 1}
        ],
        "challenge": {"question": "Is it possible to reverse a quantum gate operation?", "options": ["Never", "Always (Quantum gates are reversible)", "Only if the computer is off", "Yes, but it takes 100 years"], "answer": 1},
        "fact": "Did you know? Indian startups like QNu Labs are already using quantum-inspired gates to create unhackable communication systems."
    },
    "topic_3": {
        "title": "Superposition and Entanglement",
        "explanation": """
        **Superposition** is the ability of a qubit to be 'both' at once. But **Entanglement** is even stranger. It is a unique quantum connection between two qubits. When two qubits are entangled, the state of one is instantly connected to the state of the other, no matter how far apart they are.

        Einstein called this 'spooky action at a distance.' If you measure one entangled qubit and find it is '1', you instantly know the other one is '0', even if it is on the other side of the galaxy. This connection allows quantum computers to share information across their internal systems with incredible efficiency.

        Together, Superposition and Entanglement are the 'engines' of quantum power. Superposition lets the computer explore many paths at once, while Entanglement lets different parts of the computer work together in total harmony.
        """,
        "india_example": "ISRO (Indian Space Research Organisation) successfully demonstrated 'Quantum Entanglement' across a distance of 300 meters in Ahmedabad, a first step toward a secure 'Quantum Satellite' network.",
        "key_terms": [
            {"term": "Entanglement", "definition": "A phenomenon where two qubits become linked and share the same fate."},
            {"term": "Measurement", "definition": "The act of looking at a qubit, which forces it to choose a state (0 or 1)."},
            {"term": "Spooky Action", "definition": "Einstein's term for the instant connection seen in entanglement."},
            {"term": "Quantum Teleportation", "definition": "Using entanglement to transfer information instantly across distances."},
            {"term": "Complexity", "definition": "A measure of how difficult a problem is for a computer to solve."}
        ],
        "quiz": [
            {"question": "What did Einstein call entanglement?", "options": ["Magic math", "Spooky action at a distance", "Quantum speed", "The invisible wire"], "answer": 1},
            {"question": "If two qubits are entangled and you measure one, what happens to the other?", "options": ["Nothing", "It instantly reacts", "It gets deleted", "It gets hot"], "answer": 1},
            {"question": "Why is entanglement useful?", "options": ["It makes computers look cool", "It allows parts of a computer to work in harmony", "It reduces electricity use", "It saves disk space"], "answer": 1}
        ],
        "challenge": {"question": "Does entanglement allow for faster-than-light communication of actual data?", "options": ["Yes", "No (Information still requires a classical channel)", "Only for ISRO", "On Sundays"], "answer": 1},
        "fact": "Did you know? In 2022, ISRO broke records by achieving secure quantum communication over free space, proving India's leadership in this 'spooky' tech."
    },
    "topic_4": {
        "title": "Quantum Circuits",
        "explanation": """
        A **Quantum Circuit** is like a map or a recipe for a quantum computer. It is a sequence of quantum gates applied to a set of qubits to solve a specific problem. Just like you follow steps to bake a cake, a quantum circuit follows steps to find an answer.

        These circuits are represented as lines (wires) and boxes (gates). The qubits start on the left, pass through various gates in the middle, and are finally 'measured' on the right. Measurement is the final step where the quantum magic stops, and we get a normal result we can read.

        Designing these circuits is hard because you have to balance the complexity of the calculation against the risk of the system losing its quantum state (decoherence) before the task is finished.
        """,
        "india_example": "The 'Quantum Computing Lab' at IIT Madras provides students with access to real quantum computers via the cloud to practice building their own quantum circuits.",
        "key_terms": [
            {"term": "Quantum Wire", "definition": "Represents the path of a qubit through time in a circuit diagram."},
            {"term": "Oracle", "definition": "A special part of a quantum circuit that 'knows' the answer to a specific question."},
            {"term": "Algorithmic Depth", "definition": "The number of gates a qubit passes through in a circuit."},
            {"term": "Readout", "definition": "The final step of a circuit where results are translated to classical data."},
            {"term": "Optimization", "definition": "The process of making a circuit shorter and more efficient."}
        ],
        "quiz": [
            {"question": "On a quantum circuit diagram, what do the lines represent?", "options": ["Electricity", "The path of a qubit (time)", "Cooling pipes", "Internet cables"], "answer": 1},
            {"question": "Where does 'measurement' usually happen in a circuit?", "options": ["The beginning", "The middle", "The end", "Nowhere"], "answer": 1},
            {"question": "What is the goal of quantum circuit optimization?", "options": ["Making it look pretty", "Making it shorter and more efficient", "Adding more gates", "Changing the color"], "answer": 1}
        ],
        "challenge": {"question": "What happens if a quantum circuit is too deep (too many gates)?", "options": ["It gets faster", "Errors accumulate and decoherence occurs", "It turns into a bit", "It prints more paper"], "answer": 1},
        "fact": "Did you know? India is setting up a 'Quantum Circuit Repository' to share standardized research code between different IITs."
    },
    "topic_5": {
        "title": "Quantum Algorithms in India",
        "explanation": """
        India is one of the few countries in the world with a dedicated **National Quantum Mission**. This mission isn't just about building computers; it's about using **Quantum Algorithms** to solve real-world problems like predicting weather, creating new medicines, and securing our digital borders.

        Quantum algorithms are specialized sets of instructions that take advantage of superposition and entanglement. For example, 'Grover’s Algorithm' can search through a massive database much faster than any normal computer, while 'Shor’s Algorithm' could potentially crack modern internet security.

        Indian scientists at organizations like C-DAC and ISRO are working on 'Post-Quantum Cryptography'—a way to build security that even a powerful quantum computer can't break. This is vital for protecting India's national data in the future.
        """,
        "india_example": "C-DAC (Centre for Development of Advanced Computing) in Pune is developing quantum simulators to help Indian industries prepare for the 'Quantum Age.'",
        "key_terms": [
            {"term": "Algorithm", "definition": "A set of instructions to solve a problem."},
            {"term": "Cryptography", "definition": "The art of writing or solving codes to protect information."},
            {"term": "Isro", "definition": "India's space agency, a pioneer in quantum satellite communication."},
            {"term": "C-DAC", "definition": "India's premier R&D organization for advanced computing."},
            {"term": "Post-Quantum", "definition": "Technology designed to be secure against future quantum computers."}
        ],
        "quiz": [
            {"question": "What is the primary goal of India's National Quantum Mission?", "options": ["To build better phones", "To develop quantum tech for the nation", "To launch more satellites", "To increase internet speed"], "answer": 1},
            {"question": "Which organization is developing quantum simulators in Pune?", "options": ["ISRO", "C-DAC", "NASA", "Google"], "answer": 1},
            {"question": "Why is 'Post-Quantum Cryptography' important?", "options": ["It's faster", "It's secure against future quantum attacks", "It uses less power", "It's free"], "answer": 1}
        ],
        "challenge": {"question": "Which Indian algorithm initiative is focused on simulation?", "options": ["ISRO-Sky", "QSim by MeitY", "IIT-Net", "C-DAC-Super"], "answer": 1},
        "fact": "Did you know? India's first indigenous quantum computer simulator, called 'QSim,' was launched by the MeitY (Ministry of Electronics and Information Technology) to train thousands of students."
    }
}
