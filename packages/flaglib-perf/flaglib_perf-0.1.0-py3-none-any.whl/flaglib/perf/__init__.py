def record(
    command: list[str] | None = None,
    event: str | None = None,
    filter_str: str | None = None,
    exclude_perf: bool = False,
    all_cpus: bool = False,
    pid: list[str] | None = None,
    tid: list[str] | None = None,
    uid: str | None = None,
    realtime: str | None = None,
    no_buffering: bool = False,
    count: str | None = None,
    output: str | None = None,
    no_inherit: bool = False,
    freq: str | None = None,
    strict_freq: bool = False,
    mmap_pages: str | None = None,
    call_graph: str | None = None,
    quiet: bool = False,
    verbose: bool = False,
    stat: bool = False,
    data: bool = False,
    phys_data: bool = False,
    data_page_size: bool = False,
    code_page_size: bool = False,
    timestamp: bool = False,
    period: bool = False,
    sample_cpu: bool = False,
    sample_identifier: bool = False,
    no_samples: bool = False,
    raw_samples: bool = False,
    cpu: str | None = None,
    no_buildid: bool = False,
    no_buildid_cache: bool = False,
    cgroup: list[str] | None = None,
    branch_any: bool = False,
    branch_filter: str | None = None,
    weight: bool = False,
    namespaces: bool = False,
    all_cgroups: bool = False,
    transaction: bool = False,
    per_thread: bool = False,
    delay: str | None = None,
    intr_regs: str | None = None,
    user_regs: str | None = None,
    running_time: bool = False,
    clockid: str | None = None,
    snapshot: str | None = None,
    aux_sample: str | None = None,
    proc_map_timeout: str | None = None,
    switch_events: bool = False,
    vmlinux: str | None = None,
    buildid_all: bool = False,
    buildid_mmap: bool = False,
    aio: str | None = None,
    affinity: str | None = None,
    mmap_flush: str | None = None,
    compression_level: int | None = None,
    all_kernel: bool = False,
    all_user: bool = False,
    kernel_callchains: bool = False,
    user_callchains: bool = False,
    timestamp_filename: bool = False,
    timestamp_boundary: bool = False,
    switch_output: str | None = None,
    switch_output_event: str | None = None,
    switch_max_files: int | None = None,
    dry_run: bool = False,
    synth: str | None = None,
    tail_synthesize: bool = False,
    overwrite: bool = False,
    kcore: bool = False,
    max_size: str | None = None,
    num_thread_synthesize: int | None = None,
    control: str | None = None,
    threads: str | None = None,
    debuginfod: str | None = None,
    off_cpu: bool = False,
    setup_filter: str | None = None,
) -> list[str]:
    """
    Generate arguments for the perf CLI tool based on provided options.

    Args:
        command: List of commands to profile
        event: Event selector (-e/--event)
        filter_str: Event filter (--filter)
        exclude_perf: Don't record perf events (--exclude-perf)
        all_cpus: System-wide collection (--all-cpus)
        pid: Process IDs to monitor (--pid)
        tid: Thread IDs to monitor (--tid)
        uid: User IDs to monitor (--uid)
        realtime: Realtime priority (--realtime)
        no_buffering: Disable buffering (--no-buffering)
        count: Event period to sample (--count)
        output: Output file name (--output)
        no_inherit: Disable inheritance (--no-inherit)
        freq: Sampling frequency (--freq)
        strict_freq: Fail if frequency can't be used (--strict-freq)
        mmap_pages: Number of mmap pages (--mmap-pages)
        call_graph: Call graph options (--call-graph)
        quiet: Suppress output (--quiet)
        verbose: Verbose output (--verbose)
        stat: Record per-thread counts (--stat)
        data: Record sample addresses (--data)
        phys_data: Record physical addresses (--phys-data)
        data_page_size: Record data page size (--data-page-size)
        code_page_size: Record code page size (--code-page-size)
        timestamp: Record timestamps (--timestamp)
        period: Record sample period (--period)
        sample_cpu: Record sample CPU (--sample-cpu)
        sample_identifier: Record sample identifier (--sample-identifier)
        no_samples: Don't sample (--no-samples)
        raw_samples: Collect raw samples (--raw-samples)
        cpu: CPUs to monitor (--cpu)
        no_buildid: Don't save buildids (--no-buildid)
        no_buildid_cache: Don't update buildid cache (--no-buildid-cache)
        cgroup: Cgroups to monitor (--cgroup)
        branch_any: Enable branch stack sampling (--branch-any)
        branch_filter: Branch filter options (--branch-filter)
        weight: Enable weighted sampling (--weight)
        namespaces: Record namespace events (--namespaces)
        all_cgroups: Record cgroup events (--all-cgroups)
        transaction: Record transaction flags (--transaction)
        per_thread: Use per-thread mmaps (--per-thread)
        delay: Delay before measuring (--delay)
        intr_regs: Capture interrupt registers (--intr-regs)
        user_regs: Capture user registers (--user-regs)
        running_time: Record running time (--running-time)
        clockid: Clock to use (--clockid)
        snapshot: AUX snapshot mode (--snapshot)
        aux_sample: AUX sampling (--aux-sample)
        proc_map_timeout: /proc map timeout (--proc-map-timeout)
        switch_events: Record context switch events (--switch-events)
        vmlinux: Path to vmlinux (--vmlinux)
        buildid_all: Record all buildids (--buildid-all)
        buildid_mmap: Record buildids in mmap2 (--buildid-mmap)
        aio: Asynchronous I/O mode (--aio)
        affinity: Affinity mode (--affinity)
        mmap_flush: Mmap flush threshold (--mmap-flush)
        compression_level: Compression level (--compression-level)
        all_kernel: Run all events in kernel (--all-kernel)
        all_user: Run all events in user (--all-user)
        kernel_callchains: Kernel-only callchains (--kernel-callchains)
        user_callchains: User-only callchains (--user-callchains)
        timestamp_filename: Add timestamp to filename (--timestamp-filename)
        timestamp_boundary: Record timestamp boundary (--timestamp-boundary)
        switch_output: Switch output mode (--switch-output)
        switch_output_event: Event to trigger output switch (--switch-output-event)
        switch_max_files: Max output files (--switch-max-files)
        dry_run: Parse options then exit (--dry-run)
        synth: Event synthesis (--synth)
        tail_synthesize: Synthesize at end (--tail-synthesize)
        overwrite: Use overwritable buffer (--overwrite)
        kcore: Copy /proc/kcore (--kcore)
        max_size: Max sample size (--max-size)
        num_thread_synthesize: Synthesis threads (--num-thread-synthesize)
        control: Control interface (--control)
        threads: Thread configuration (--threads)
        debuginfod: Debuginfod URL (--debuginfod)
        off_cpu: Enable off-cpu profiling (--off-cpu)
        setup_filter: Setup BPF filter (--setup-filter)

    Returns:
        List of command line arguments for perf

    Examples:
        >>> record(command=["./my_program"], event="cycles", output="perf.data")
        ['-e', 'cycles', '-o', 'perf.data', '--', './my_program']

        >>> record(command=["./benchmark"], all_cpus=True, freq="1000", call_graph="dwarf")
        ['-a', '-F', '1000', '--call-graph', 'dwarf', '--', './benchmark']

        >>> record(pid=["1234"], event="cycles,instructions", data=True)
        ['-e', 'cycles,instructions', '-p', '1234', '-d']

        >>> record(command=["sleep", "10"], cpu="0-3", switch_events=True)
        ['-C', '0-3', '--switch-events', '--', 'sleep', '10']

        >>> record(all_cpus=True, event="cache-misses", no_inherit=True, timestamp=True)
        ['-e', 'cache-misses', '-a', '-i', '-T']

        >>> record(command=["./app"], cgroup=["group1", "group2"])
        ['-G', 'group1,group2', '--', './app']

        >>> record(command=["python", "script.py"], compression_level=9, verbose=True)
        ['-v', '-z', '9', '--', 'python', 'script.py']
    """
    args = []

    # Add options
    if event:
        args.extend(['-e', event])
    if filter_str:
        args.extend(['--filter', filter_str])
    if exclude_perf:
        args.append('--exclude-perf')
    if all_cpus:
        args.append('-a')
    if pid:
        args.extend(['-p', ','.join(pid)])
    if tid:
        args.extend(['-t', ','.join(tid)])
    if uid:
        args.extend(['-u', uid])
    if realtime:
        args.extend(['-r', realtime])
    if no_buffering:
        args.append('--no-buffering')
    if count:
        args.extend(['-c', count])
    if output:
        args.extend(['-o', output])
    if no_inherit:
        args.append('-i')
    if freq:
        args.extend(['-F', freq])
    if strict_freq:
        args.append('--strict-freq')
    if mmap_pages:
        args.extend(['-m', mmap_pages])
    if call_graph:
        args.extend(['--call-graph', call_graph])
    if quiet:
        args.append('-q')
    if verbose:
        args.append('-v')
    if stat:
        args.append('-s')
    if data:
        args.append('-d')
    if phys_data:
        args.append('--phys-data')
    if data_page_size:
        args.append('--data-page-size')
    if code_page_size:
        args.append('--code-page-size')
    if timestamp:
        args.append('-T')
    if period:
        args.append('-P')
    if sample_cpu:
        args.append('--sample-cpu')
    if sample_identifier:
        args.append('--sample-identifier')
    if no_samples:
        args.append('-n')
    if raw_samples:
        args.append('-R')
    if cpu:
        args.extend(['-C', cpu])
    if no_buildid:
        args.append('-B')
    if no_buildid_cache:
        args.append('-N')
    if cgroup:
        args.extend(['-G', ','.join(cgroup)])
    if branch_any:
        args.append('-b')
    if branch_filter:
        args.extend(['-j', branch_filter])
    if weight:
        args.append('-W')
    if namespaces:
        args.append('--namespaces')
    if all_cgroups:
        args.append('--all-cgroups')
    if transaction:
        args.append('--transaction')
    if per_thread:
        args.append('--per-thread')
    if delay:
        args.extend(['-D', delay])
    if intr_regs:
        args.extend(['-I', intr_regs])
    if user_regs:
        args.extend(['--user-regs', user_regs])
    if running_time:
        args.append('--running-time')
    if clockid:
        args.extend(['-k', clockid])
    if snapshot:
        args.extend(['-S', snapshot])
    if aux_sample:
        args.extend(['--aux-sample', aux_sample])
    if proc_map_timeout:
        args.extend(['--proc-map-timeout', proc_map_timeout])
    if switch_events:
        args.append('--switch-events')
    if vmlinux:
        args.extend(['--vmlinux', vmlinux])
    if buildid_all:
        args.append('--buildid-all')
    if buildid_mmap:
        args.append('--buildid-mmap')
    if aio:
        args.extend(['--aio', aio])
    if affinity:
        args.extend(['--affinity', affinity])
    if mmap_flush:
        args.extend(['--mmap-flush', mmap_flush])
    if compression_level is not None:
        args.extend(['-z', str(compression_level)])
    if all_kernel:
        args.append('--all-kernel')
    if all_user:
        args.append('--all-user')
    if kernel_callchains:
        args.append('--kernel-callchains')
    if user_callchains:
        args.append('--user-callchains')
    if timestamp_filename:
        args.append('--timestamp-filename')
    if timestamp_boundary:
        args.append('--timestamp-boundary')
    if switch_output:
        args.extend(['--switch-output', switch_output])
    if switch_output_event:
        args.extend(['--switch-output-event', switch_output_event])
    if switch_max_files is not None:
        args.extend(['--switch-max-files', str(switch_max_files)])
    if dry_run:
        args.append('--dry-run')
    if synth:
        args.extend(['--synth', synth])
    if tail_synthesize:
        args.append('--tail-synthesize')
    if overwrite:
        args.append('--overwrite')
    if kcore:
        args.append('--kcore')
    if max_size:
        args.extend(['--max-size', max_size])
    if num_thread_synthesize is not None:
        args.extend(['--num-thread-synthesize', str(num_thread_synthesize)])
    if control:
        args.extend(['--control', control])
    if threads:
        args.extend(['--threads', threads])
    if debuginfod:
        args.extend(['--debuginfod', debuginfod])
    if off_cpu:
        args.append('--off-cpu')
    if setup_filter:
        args.extend(['--setup-filter', setup_filter])

    if command:
        args.extend(['--', *command])
    return args
