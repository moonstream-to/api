package main

import (
	"context"
	"fmt"

	"github.com/spf13/cobra"

	workers "github.com/moonstream-to/api/workers/pkg"
	engine "github.com/moonstream-to/api/workers/pkg/engine"
)

func CreateRootCommand() *cobra.Command {
	// rootCmd represents the base command when called without any subcommands
	rootCmd := &cobra.Command{
		Use:   "workers",
		Short: "Autonomous workers for moonstream services",
		Long: `workers is a CLI that allows you to run multiple operations according to Moonstream services.

	workers currently supports services:
	- Engine
	`,
		Run: func(cmd *cobra.Command, args []string) {},
	}

	versionCmd := CreateVersionCommand()
	engineCmd := CreateEngineCommand()
	rootCmd.AddCommand(versionCmd, engineCmd)

	completionCmd := CreateCompletionCommand(rootCmd)
	rootCmd.AddCommand(completionCmd)

	return rootCmd
}

func CreateCompletionCommand(rootCmd *cobra.Command) *cobra.Command {
	completionCmd := &cobra.Command{
		Use:   "completion",
		Short: "Generate shell completion scripts for workers",
		Long: `Generate shell completion scripts for workers.

The command for each shell will print a completion script to stdout. You can source this script to get
completions in your current shell session. You can add this script to the completion directory for your
shell to get completions for all future sessions.

For example, to activate bash completions in your current shell:
		$ . <(workers completion bash)

To add workers completions for all bash sessions:
		$ workers completion bash > /etc/bash_completion.d/workers_completions`,
	}

	bashCompletionCmd := &cobra.Command{
		Use:   "bash",
		Short: "bash completions for workers",
		Run: func(cmd *cobra.Command, args []string) {
			rootCmd.GenBashCompletion(cmd.OutOrStdout())
		},
	}

	zshCompletionCmd := &cobra.Command{
		Use:   "zsh",
		Short: "zsh completions for workers",
		Run: func(cmd *cobra.Command, args []string) {
			rootCmd.GenZshCompletion(cmd.OutOrStdout())
		},
	}

	fishCompletionCmd := &cobra.Command{
		Use:   "fish",
		Short: "fish completions for workers",
		Run: func(cmd *cobra.Command, args []string) {
			rootCmd.GenFishCompletion(cmd.OutOrStdout(), true)
		},
	}

	powershellCompletionCmd := &cobra.Command{
		Use:   "powershell",
		Short: "powershell completions for workers",
		Run: func(cmd *cobra.Command, args []string) {
			rootCmd.GenPowerShellCompletion(cmd.OutOrStdout())
		},
	}

	completionCmd.AddCommand(bashCompletionCmd, zshCompletionCmd, fishCompletionCmd, powershellCompletionCmd)

	return completionCmd
}

func CreateVersionCommand() *cobra.Command {
	versionCmd := &cobra.Command{
		Use:   "version",
		Short: "Print the version number of workers",
		Long:  `All software has versions. This is workers's`,
		Run: func(cmd *cobra.Command, args []string) {
			cmd.Println(workers.VERSION)
		},
	}
	return versionCmd
}

func CreateEngineCommand() *cobra.Command {
	engineCommand := &cobra.Command{
		Use:   "engine",
		Short: "Engine workers and more",
	}

	var dbUri string
	engineCommand.PersistentFlags().StringVarP(&dbUri, "db-uri", "d", "", "Database URI.")

	cleanCallRequestsCommand := &cobra.Command{
		Use:   "clean-call-requests",
		Short: "Clean all inactive call requests from database.",
		Long:  "Remove records in call_requests database table with ttl value greater then now.",
		RunE: func(cmd *cobra.Command, args []string) error {
			ctx := context.Background()

			dbPool, err := CreateDbPool(ctx, dbUri, "10s")
			if err != nil {
				return fmt.Errorf("database connection error: %v", err)
			}
			defer dbPool.Close()

			return engine.CleanCallRequestsCommand(ctx, dbPool)
		},
	}

	engineCommand.AddCommand(cleanCallRequestsCommand)

	return engineCommand
}
