#!/usr/bin/env bash
set -euo pipefail

PROFILE=aws_second
REGION=ap-south-1
ROLE=github-actions-ai-docker
ACCOUNT=357275711997
PROVIDER="arn:aws:iam::${ACCOUNT}:oidc-provider/token.actions.githubusercontent.com"

if ! aws --profile "$PROFILE" iam get-open-id-connect-provider --open-id-connect-provider-arn "$PROVIDER" >/dev/null 2>&1; then
  aws --profile "$PROFILE" iam create-open-id-connect-provider \
    --url https://token.actions.githubusercontent.com \
    --client-id-list sts.amazonaws.com \
    --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1 >/dev/null
fi

if aws --profile "$PROFILE" iam get-role --role-name "$ROLE" >/dev/null 2>&1; then
  aws --profile "$PROFILE" iam update-assume-role-policy \
    --role-name "$ROLE" \
    --policy-document file://infra/github-actions-trust-policy.json
else
  aws --profile "$PROFILE" iam create-role \
    --role-name "$ROLE" \
    --assume-role-policy-document file://infra/github-actions-trust-policy.json \
    --description "GitHub Actions ECR publishing for github-actions-ai-docker" >/dev/null
fi

aws --profile "$PROFILE" iam put-role-policy \
  --role-name "$ROLE" \
  --policy-name ecr-publish \
  --policy-document file://infra/github-actions-ecr-policy.json

aws --profile "$PROFILE" iam get-role --role-name "$ROLE" \
  --query 'Role.Arn' --output text
