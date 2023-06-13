package main

import (
	"context"
	"fmt"

	"github.com/spf13/cobra"

	probes "github.com/moonstream-to/api/probes/pkg"
	engine "github.com/moonstream-to/api/probes/pkg/engine"
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
	serviceCmd := CreateServiceCommand()
	rootCmd.AddCommand(versionCmd, engineCmd, serviceCmd)

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
		Long:  `All software has versions. This is workers's.`,
		Run: func(cmd *cobra.Command, args []string) {
			cmd.Println(probes.VERSION)
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
	var dbTimeout string
	engineCommand.PersistentFlags().StringVarP(&dbUri, "db-uri", "d", "", "Database URI")
	engineCommand.PersistentFlags().StringVarP(&dbTimeout, "db-timeout", "t", "", "Database timeout (format: 10s)")
	engineCommand.MarkFlagRequired("db-uri")

	for _, sc := range engine.ENGINE_SUPPORTED_WORKERS {
		tempCommand := &cobra.Command{
			Use:   sc.Name,
			Short: sc.Description,
			Long:  sc.LonDescription,
			RunE: func(cmd *cobra.Command, args []string) error {
				ctx := context.Background()

				dbPool, err := CreateDbPool(ctx, dbUri, dbTimeout)
				if err != nil {
					return fmt.Errorf("database connection error: %v", err)
				}
				defer dbPool.Close()

				return sc.ExecFunction(ctx, dbPool)
			},
		}
		engineCommand.AddCommand(tempCommand)
	}

	return engineCommand
}

func CreateServiceCommand() *cobra.Command {
	var configPaths []string

	serviceCmd := &cobra.Command{
		Use:   "service",
		Short: "Run workers as background asynchronous services",
		Long:  `Each active worker specified in configuration will run in go-routine.`,
		RunE: func(cmd *cobra.Command, args []string) error {
			return RunService(configPaths)
		},
	}

	serviceCmd.PersistentFlags().StringSliceVarP(&configPaths, "config", "c", []string{}, "Config paths")

	return serviceCmd
}
