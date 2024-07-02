# Web Status Monitor
> This project develops a web status monitor (simplified version of uptimerobot.com) to practice web programming and understand the web related protocols: HTTP and TLS/SSL.
> - Implements HTTP client socket to interact with the web server
> - Doesn't use any existing HTTP client library
> - Uses an existing SSL library to help implement the HTTPS client (extra credit)

## Requirements
- [x] <a target="_blank" href="https://docs.continuum.io/free/anaconda/install">Anaconda</a> **OR** <a target="_blank" href="https://docs.conda.io/projects/miniconda/en/latest">Miniconda</a>

> [!TIP]
> If you have trouble deciding between Anaconda and Miniconda, please refer to the table below:
> <table>
>  <thead>
>   <tr>
>    <th><center>Anaconda</center></th>
>    <th><center>Miniconda</center></th>
>   </tr>
>  </thead>
>  <tbody>
>   <tr>
>    <td>New to conda and/or Python</td>
>    <td>Familiar with conda and/or Python</td>
>   </tr>
>   <tr>
>    <td>Not familiar with using terminal and prefer GUI</td>
>    <td>Comfortable using terminal</td>
>   </tr>
>   <tr>
>    <td>Like the convenience of having Python and 1,500+ scientific packages automatically installed at once</td>
>    <td>Want fast access to Python and the conda commands and plan to sort out the other programs later</td>
>   </tr>
>   <tr>
>    <td>Have the time and space (a few minutes and 3 GB)</td>
>    <td>Don't have the time or space to install 1,500+ packages</td>
>   </tr>
>   <tr>
>    <td>Don't want to individually install each package</td>
>    <td>Don't mind individually installing each package</td>
>   </tr>
>  </tbody>
> </table>
>
> Typing out entire Conda commands can sometimes be tedious, so I wrote a shell script ([`conda_shortcuts.sh` on GitHub Gist](https://gist.github.com/lynkos/7a4ce7f9e38bb56174360648461a3dc8)) to define shortcuts for commonly used Conda commands.
> <details>
>   <summary>Example: Delete/remove a conda environment named <code>test_env</code></summary>
>
> * Shortcut command
>     ```
>     rmenv test_env
>     ```
> * Manually typing out the entire command
>     ```sh
>     conda env remove -n test_env && rm -rf $(conda info --base)/envs/test_env
>     ```
>
> The shortcut has 80.8% fewer characters!
> </details>

## Installation
1. Verify that conda is installed
   ```
   conda --version
   ```

2. Ensure conda is up to date
   ```
   conda update conda
   ```

3. Enter the directory you want `web-status-monitor` to be cloned in
   * POSIX
      ```sh
      cd ~/path/to/directory
      ```
   * Windows
      ```sh
      cd C:\Users\user\path\to\directory
      ```

4. Clone and enter `web-status-monitor`
   ```sh
   git clone https://github.com/lynkos/web-status-monitor.git && cd web-status-monitor
   ```

5. Create virtual environment from [`environment.yml`](environment.yml)
   ```sh
   conda env create -f environment.yml
   ```

## Usage
<ol>
   <li>Activate <code>monitor</code> (i.e., virtual environment)<pre>conda activate monitor</pre></li>
   <li>Confirm <code>monitor</code> is active
      <ul>
        <li><code>monitor</code> should be in parentheses () or brackets [] before your command prompt, e.g.<pre>(monitor) $</pre></li>
        <li>See which virtual environments are available and/or currently active (active environment denoted with asterisk (*))<pre>conda info --envs</pre> <b>OR</b> <pre>conda env list</pre></li>
      </ul>
   </li>
   <li>Run <a href="monitor.py"><code>monitor.py</code></a> (<code>urls_file</code> is the path to a file containing a list of URLs)<pre>python monitor.py urls_file</pre></li>
   <li>Deactivate <code>monitor</code> (i.e., virtual environment) when finished<pre>conda deactivate</pre></li>
</ol>