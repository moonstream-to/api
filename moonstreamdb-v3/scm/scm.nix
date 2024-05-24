with builtins;
let
    scm_repos = [
        (getEnv "SCM_GIT")
        (fetchGit {
            url = "git@gitlab.com:deltaex/schematic.git";
            rev = "ba5d7b40255e5da9a74e666dd88e309dae40fbd2";
        })
    ];
    scm_repo = head (filter (x: x != "") scm_repos);
    scm = (import scm_repo {
        verbose = true;
        repos = [
            "."
            (getEnv "MDP_GIT")
            (fetchGit {
                url = "git@github.com:moonstream-to/api.git";
                rev = "e27476ac5327d5494d2db16bb9bf781f9fc14e41";
            })
        ] ++ scm_repos;
    });
in rec {
    schematic = scm.shell.overrideAttrs ( oldAttrs : {
        shellHook = oldAttrs.shellHook + ''
            [ -n "$ENV" -a "$ENV" != "dev" ]
            source /home/moonstream/moonstream-db-v3-indexes-secrets/pg.env
        '';
    });
}
