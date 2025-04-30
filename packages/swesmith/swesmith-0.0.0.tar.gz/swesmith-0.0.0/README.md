<p align="center">
  <a href="http://swe-bench.github.io">
    <img src="docs/assets/banner.png" style="height: 10em" alt="Kawhi the SWE-smith" />
  </a>
</p>

<br>

<div align="center">
<a href="https://www.python.org/">
    <img alt="Build" src="https://img.shields.io/badge/Python-3.10+-1f425f.svg?color=purple">
</a>
<a href="https://copyright.princeton.edu/policy">
    <img alt="License" src="https://img.shields.io/badge/License-MIT-blue">
</a>
</div>

<hr />

SWE-smith is a toolkit for training software engineering (SWE) agents. With SWE-smith, you can:
* Create an *unlimited* number of [SWE-bench](https://github.com/SWE-bench/SWE-bench) style task instances (bug reports with solution validation) for any Python repository.
* *Generate trajectories* of [SWE-agent](https://github.com/SWE-agent/SWE-agent) (running on top of an LM like GPT-4o or Claude 3.7) solving those task instances. 
* *Train local LMs* on these trajectories to improve their performance on software engineering tasks (resulting in models like [SWE-agent-LM-32B]())

### 🚀 Get Started
Check out the [documentation]() for a complete guide on how to use SWE-smith, including
* How to [install]() the repository locally or as a PyPI package.
* [Create Task Instances]() for any Python repository with SWE-smith.
* Use your task instance to [train your own SWE-agents]()

### 💿 Resources
In addition to this toolkit, we've also provided several artifacts on the [SWE-bench HuggingFace](https://huggingface.co/SWE-bench), including:
* [50k Python Task Instances](https://huggingface.co/datasets/SWE-bench/SWE-smith), created using SWE-smith.
* [SWE-agent-LM-32B](https://huggingface.co/SWE-bench/SWE-agent-LM-32B), trained using SWE-smith. Achieves **40.2%** pass@1 on [SWE-bench Verified](https://huggingface.co/datasets/SWE-bench/SWE-bench_Verified)!
* [5k Trajectories](https://huggingface.co/datasets/SWE-bench/SWE-smith-trajs-250429) that SWE-agent-LM-32B was trained on.

And there's more coming!

### 💫 Contributions
Excited about SWE-smith? We're actively working on several follow ups, and love meaningful collaborations! What we're thinking about...
* Make SWE-smith work for non-Python languages
* New bug generation techniques
* Train SWE-agents with more 

Contact Person: [John Yang](https://john-b-yang.github.io/), [Kilian Lieret](https://www.lieret.net/), [Carlos E. Jimenez](https://carlosejimenez.github.io/)
(Email: [johnby@stanford.edu](mailto:johnby@stanford.edu))

### 🪪 License
MIT. Check `LICENSE` for more information.

### ✍️ Citation

```
@misc{yang2025swesmith,
  title={SWE-smith: Scaling Data for Software Engineering Agents},
  author={John Yang and Kilian Lieret and Carlos E. Jimenez and Alexander Wettig and Kabir Khandpur and Yanzhe Zhang and Binyuan Hui and Ofir Press and Ludwig Schmidt and Diyi Yang},
  year={2025},
  archivePrefix={arXiv},
  primaryClass={cs.SE},
}
```
