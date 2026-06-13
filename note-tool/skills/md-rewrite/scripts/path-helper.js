#!/usr/bin/env node

/**
 * 路径计算辅助脚本
 *
 * 根据 source_file_path 推导出 Skill 需要的所有路径变量
 */

const path = require('path');

/**
 * 计算所有路径变量
 * @param {string} sourceFilePath - 源文件路径（绝对或相对）
 * @returns {Object} 包含所有路径变量的对象
 */
function calculatePaths(sourceFilePath) {
  // 规范化路径
  const normalizedSourcePath = path.normalize(sourceFilePath);

  // 提取路径组成部分
  const sourceFileDir = path.dirname(normalizedSourcePath);
  const sourceFileName = path.basename(normalizedSourcePath, path.extname(normalizedSourcePath));

  // 推导工作区目录
  const workspaceDirectory = path.join(sourceFileDir, 'workspace', sourceFileName);

  // 推导改写文件路径
  const rewrittenFilePath = path.join(sourceFileDir, `${sourceFileName}_rewritten.md`);

  // 推导备份文件路径
  const backupFilePath = path.join(sourceFileDir, `${sourceFileName}_backup.md`);

  return {
    source_file_path: normalizedSourcePath,
    source_file_dir: sourceFileDir,
    source_file_name: sourceFileName,
    workspace_directory: workspaceDirectory,
    rewritten_file_path: rewrittenFilePath,
    backup_file_path: backupFilePath,
  };
}

/**
 * 打印路径计算结果
 * @param {Object} paths - 路径对象
 */
function printPaths(paths) {
  console.log('路径推导结果：\n');
  console.log('输入参数：');
  console.log(`  source_file_path      = "${paths.source_file_path}"`);
  console.log('\n推导结果：');
  console.log(`  source_file_dir      = "${paths.source_file_dir}"`);
  console.log(`  source_file_name     = "${paths.source_file_name}"`);
  console.log(`  workspace_directory  = "${paths.workspace_directory}"`);
  console.log(`  rewritten_file_path   = "${paths.rewritten_file_path}"`);
  console.log(`  backup_file_path      = "${paths.backup_file_path}"`);
}

/**
 * 打印路径推导表格
 * @param {Object} paths - 路径对象
 */
function printPathTable(paths) {
  console.log('\n路径推导表：\n');
  console.log('┌─────────────────────────┬──────────────────────────────────────────────┐');
  console.log('│ 变量名                   │ 推导方式                                     │');
  console.log('├─────────────────────────┼──────────────────────────────────────────────┤');
  console.log(`│ source_file_path         │ 用户输入                                     │`);
  console.log(`│                         │ "${paths.source_file_path}"                │`);
  console.log('├─────────────────────────┼──────────────────────────────────────────────┤');
  console.log(`│ source_file_dir          │ 取 source_file_path 的父目录                 │`);
  console.log(`│                         │ "${paths.source_file_dir}"                  │`);
  console.log('├─────────────────────────┼──────────────────────────────────────────────┤');
  console.log(`│ source_file_name         │ 取 source_file_path 的文件名（不含扩展名）    │`);
  console.log(`│                         │ "${paths.source_file_name}"                 │`);
  console.log('├─────────────────────────┼──────────────────────────────────────────────┤');
  console.log(`│ workspace_directory     │ 拼接：source_file_dir + "workspace/" +      │`);
  console.log(`│                         │       source_file_name + "/"                  │`);
  console.log(`│                         │ "${paths.workspace_directory}"              │`);
  console.log('├─────────────────────────┼──────────────────────────────────────────────┤');
  console.log(`│ rewritten_file_path      │ 拼接：source_file_dir + source_file_name +  │`);
  console.log(`│                         │       "_rewritten.md"                         │`);
  console.log(`│                         │ "${paths.rewritten_file_path}"               │`);
  console.log('├─────────────────────────┼──────────────────────────────────────────────┤');
  console.log(`│ backup_file_path         │ 拼接：source_file_dir + source_file_name +  │`);
  console.log(`│                         │       "_backup.md"                           │`);
  console.log(`│                         │ "${paths.backup_file_path}"                  │`);
  console.log('└─────────────────────────┴──────────────────────────────────────────────┘');
}

/**
 * 导出为 JSON
 * @param {Object} paths - 路径对象
 * @returns {string} JSON 字符串
 */
function exportToJSON(paths) {
  return JSON.stringify(paths, null, 2);
}

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.log('用法：node path-helper.js <source_file_path>');
    console.log('示例：node path-helper.js "./tech_note/codex.md"');
    process.exit(1);
  }

  const sourceFilePath = args[0];
  const paths = calculatePaths(sourceFilePath);

  printPaths(paths);
  printPathTable(paths);

  // 输出 JSON 格式（用于程序调用）
  if (args.includes('--json')) {
    console.log('\nJSON 输出：\n');
    console.log(exportToJSON(paths));
  }
}

// 导出函数供其他模块使用
module.exports = {
  calculatePaths,
  printPaths,
  printPathTable,
  exportToJSON,
};
