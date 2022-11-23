#!/bin/sh

run_on_load() {
    python3 on_load.py >"harpoon-re-$(uname -n).json" <"harpoon-gen-$(uname -n).json"
}

run_on_save() {
    python3 on_save.py >"harpoon-gen-$(uname -n).json" <"harpoon-$(uname -n).json"
}

run() {
    [ ! -f "harpoon-$(uname -n).json" ] && return 1
    run_on_save
    run_on_load
}
