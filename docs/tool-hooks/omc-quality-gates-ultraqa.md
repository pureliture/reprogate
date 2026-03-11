# Verification-Loop Enforcement Model

> Status: Active
> Version: `1.0.0`

## Purpose

Some toolchains enforce AI Ops primarily through verification stages and repeated quality loops rather than pre-execution denial hooks.
This document defines that portable model.

## Core Idea

Work is not complete when execution ends.
A verification-loop adapter keeps work moving through review, verification, and repair until quality criteria are met or the workflow stops explicitly.

## Required Behavior

A conforming verification-loop adapter should:

1. connect execution work to a verification stage,
2. capture verification findings in a durable artifact,
3. repeat fix-and-verify cycles when criteria fail,
4. respect the minimum logical-role profile for team-capable processes,
5. and still pass a final repository-boundary compliance check.

## Evidence Expectations

The adapter should preserve enough evidence to answer:

- what was verified,
- what failed,
- what was fixed,
- whether another loop ran,
- and what final gate allowed completion.

## Portability Rule

Keep this document focused on workflow behavior.
Adapter docs own concrete verifier names, loop commands, state paths, and local synchronization steps.
